```markdown
# FishID 🐟

**Upload a fish photo. Get a species ID.**

![Status](https://img.shields.io/badge/status-live-brightgreen?style=flat)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat)
![Docker Pulls](https://img.shields.io/docker/pulls/binhvu3/fishid?style=flat)

🌐 **[fishid.binhtvu.com](https://fishid.binhtvu.com)**

---

## What It Does

FishID is a computer vision model that identifies Pacific and freshwater fish species from photos. Upload an image, get a species ID with confidence score and top-5 predictions in real time.

- **202 species** — Pacific coast + freshwater fish sourced from iNaturalist
- **83.3% validation accuracy** — EfficientNet-B4 trained on 180k research-grade images
- **Self-hosted** — FastAPI on Proxmox, exposed via Cloudflare tunnel
- **Live** — try it at [fishid.binhtvu.com](https://fishid.binhtvu.com)

---

## Stack

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=flat&logo=cloudflare&logoColor=white)

| Component | Tool |
|---|---|
| Model | EfficientNet-B4 (timm) |
| Training hardware | RTX 3060 (CUDA) + MacBook M4 (MPS) |
| Experiment Tracking | MLflow (self-hosted) |
| Dataset Storage | AIStor (S3-compatible, self-hosted) |
| API | FastAPI + slowapi (rate limiting) |
| Container | Docker (amd64 + arm64) |
| Deployment | Proxmox LXC + Cloudflare tunnel |

---

## Quick Start

```bash
docker pull binhvu3/fishid:latest
docker run -p 8000:8000 binhvu3/fishid:latest
```

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@fish.jpg"
```

```json
{
  "species": "Rainbow Trout",
  "scientific": "Oncorhynchus_mykiss",
  "confidence": 94.3,
  "top5": [
    { "species": "Rainbow Trout", "confidence": 94.3 },
    { "species": "Brown Trout", "confidence": 3.1 },
    { "species": "Brook Trout", "confidence": 1.4 },
    { "species": "Chinook Salmon", "confidence": 0.8 },
    { "species": "Creek Chub", "confidence": 0.4 }
  ]
}
```

---

## Model History

| Version | Model | Species | Val Accuracy | Dataset |
|---|---|---|---|---|
| v1 | EfficientNet-B0 | 9 | 99.26% | Kaggle (9k images) |
| v2 | EfficientNet-B4 | 202 | 83.3% | iNaturalist (180k images) |

**v2 species** — Pacific coast and freshwater fish including Rainbow Trout, Chinook Salmon, Largemouth Bass, Bluegill, Tidepool Sculpin, Pacific Chub Mackerel, and 196 more.

---

## Project Structure

```
fishid/
├── notebooks/
│   ├── 01_eda.ipynb                  → dataset exploration and visualization
│   ├── 02_preprocessing.ipynb        → data pipeline and transforms
│   ├── 03_training.ipynb             → original 9-species model training
│   ├── 04_evaluation.ipynb           → model evaluation and metrics
│   ├── 05_inference.ipynb            → inference and deployment prep
│   ├── 06_data_expansion.ipynb       → iNaturalist dataset download + AIStor upload
│   └── 07_retrain_expanded.ipynb     → EfficientNet-B4 retraining on 202 species
├── src/
│   ├── app.py                        → FastAPI app
│   ├── index.html                    → frontend UI
│   ├── download_samples.py           → download sample images from iNaturalist
│   └── samples/                      → sample images served by API
├── models/                           → saved model checkpoints (gitignored)
├── outputs/                          → charts and evaluation results
├── tests/
│   └── test_rate_limit.py            → rate limit tests
├── Dockerfile
├── environment.yml
└── example.env
```

---

## Development

### Setup

```bash
conda env create -f environment.yml
conda activate datascience
cp example.env .env  # fill in your AIStor and MLflow credentials
```

### Run Locally

```bash
uvicorn src.app:app --reload --port 8000
```

### Download Sample Images

```bash
python src/download_samples.py
```

### Build and Push Multi-Platform Image

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t binhvu3/fishid:latest \
  -t binhvu3/fishid:v2.0.0 \
  --push .
```

### Health Check

```bash
curl https://fishid.binhtvu.com/health
```

---

## Training

### Convert notebook to script

```bash
jupyter nbconvert --to script notebooks/07_retrain_expanded.ipynb
```

### Run training in background (GPU server)

```bash
nohup python notebooks/07_retrain_expanded.py > /workspace/models/training.log 2>&1 &
echo $! > /workspace/models/training.pid
echo "Training started with PID: $(cat /workspace/models/training.pid)"
```

### Monitor

```bash
tail -f /workspace/models/training.log            # progress
cat /workspace/models/training.pid | xargs ps -p  # check running
watch -n 1 nvidia-smi                             # GPU usage
kill $(cat /workspace/models/training.pid)        # stop
```

---

## API Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Frontend UI |
| GET | `/health` | Health check + model info |
| GET | `/samples-list` | List available sample images |
| POST | `/predict` | Predict species from uploaded image |

---

## Links

- 🌐 [Live Demo](https://fishid.binhtvu.com)
- 📖 [API Docs](https://fishid.binhtvu.com/docs)
- 🐳 [DockerHub](https://hub.docker.com/r/binhvu3/fishid)

---

## License

MIT
```