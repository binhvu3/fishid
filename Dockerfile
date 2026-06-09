FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/
COPY models/ ./models/

RUN pip install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    fastapi uvicorn python-multipart pillow python-dotenv boto3 slowapi timm

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]