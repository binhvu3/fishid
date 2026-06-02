# FishID 🐟

An image classification model that identifies fish species from photos using deep learning. Built with PyTorch and EfficientNet, trained on a labeled dataset of 9,000 images across 9 species, tracked with MLflow, and deployed as a REST API via FastAPI.

## Species
- Black Sea Sprat
- Gilt-Head Bream
- Hourse Mackerel
- Red Mullet
- Red Sea Bream
- Sea Bass
- Shrimp
- Striped Red Mullet
- Trout

## Tech Stack
- **Model:** PyTorch + EfficientNet (transfer learning)
- **Experiment Tracking:** MLflow
- **Data Storage:** AIStor (S3-compatible object storage)
- **Deployment:** FastAPI + Docker
- **Environment:** Python 3.11, Conda

## Project Structure
```
fishid/
├── notebooks/        # EDA, preprocessing, training, evaluation
├── src/              # reusable modules
├── configs/          # hyperparameters and model configs
├── models/           # saved model checkpoints
├── outputs/          # charts, plots, evaluation results
└── data/             # local data (not committed)
```

## Setup
```bash
conda env create -f environment.yml
conda activate datascience
```

## Notebooks
- `01_eda.ipynb` → dataset exploration and visualization
- `02_preprocessing.ipynb` → data pipeline and transforms
- `03_training.ipynb` → model training with MLflow tracking
- `04_evaluation.ipynb` → model evaluation and metrics
- `05_inference.ipynb` → inference and deployment prep

## Run Locally
```bash
cd src
uvicorn app:app --reload --port 8000
```

## Docker

### Build
```bash
docker build -t fishid .
```

### Run
```bash
docker run -p 8000:8000 fishid
```

## API Routes

### Health Check
```bash
curl http://localhost:8000/
```

### Predict Fish Species
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/fish.jpg"
```

### Example Response
```json
{
  "species": "Trout",
  "confidence": 61.61
}
```

## License
MIT
```