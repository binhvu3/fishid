import io
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path("../.env"))

app = FastAPI(title="FishID API")

classes = [
    "Black Sea Sprat",
    "Gilt-Head Bream",
    "Hourse Mackerel",
    "Red Mullet",
    "Red Sea Bream",
    "Sea Bass",
    "Shrimp",
    "Striped Red Mullet",
    "Trout"
]

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
BASE_DIR = Path(__file__).resolve().parent.parent
model.load_state_dict(torch.load(BASE_DIR / "models/efficientnet_b0_fish.pth", map_location=device))
model = model.to(device)
model.eval()

inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

@app.get("/")
def root():
    return {"message": "FishID API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor = inference_transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = probabilities.max(1)

    return JSONResponse({
        "species": classes[predicted.item()],
        "confidence": round(confidence.item() * 100, 2)
    })