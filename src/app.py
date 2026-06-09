import io
import os
import json
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import timm

os.environ["PYTORCH_DISABLE_NNPACK"] = "1"
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="FishID API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/samples", StaticFiles(directory=str(BASE_DIR / "src/samples")), name="samples")

# ── Load model ──
device = torch.device("cpu")
MODEL_PATH = BASE_DIR / "models/efficientnet_b4_fish_expanded.pth"

checkpoint = torch.load(MODEL_PATH, map_location=device)
classes = checkpoint['classes']
num_classes = checkpoint['num_classes']

model = timm.create_model('efficientnet_b4', pretrained=False, num_classes=num_classes)
model.load_state_dict(checkpoint['model_state_dict'])
model = model.to(device)
model.eval()

# ── Load common name mapping ──
CLASS_MAP_PATH = BASE_DIR / "models/class_to_common.json"
if CLASS_MAP_PATH.exists():
    with open(CLASS_MAP_PATH) as f:
        class_to_common = json.load(f)
else:
    class_to_common = {}

# ── Transforms ──
inference_transform = transforms.Compose([
    transforms.Resize((380, 380)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

@app.get("/")
def ui():
    return FileResponse(BASE_DIR / "src/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "model": "efficientnet_b4", "classes": num_classes}

@app.get("/samples-list")
def samples_list():
    samples_dir = BASE_DIR / "src/samples"
    return {"samples": [f.name for f in samples_dir.iterdir() if f.is_file()]}

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor = inference_transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)
        top5_probs, top5_indices = probabilities.topk(5, dim=1)

    top5 = []
    for prob, idx in zip(top5_probs[0].tolist(), top5_indices[0].tolist()):
        scientific = classes[idx]
        common = class_to_common.get(scientific, scientific.replace('_', ' '))
        top5.append({"species": common, "scientific": scientific, "confidence": round(prob * 100, 2)})

    return JSONResponse({
        "species": top5[0]["species"],
        "scientific": top5[0]["scientific"],
        "confidence": top5[0]["confidence"],
        "top5": top5
    })