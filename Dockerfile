FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src/
COPY models/ ./models/

RUN pip install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    fastapi "starlette>=1.3.1" uvicorn "python-multipart>=0.0.31" "pillow>=13.0.0" python-dotenv boto3 slowapi timm \
 && pip install --no-cache-dir --upgrade setuptools "wheel>=0.46.2" "jaraco.context>=6.1.0"

RUN useradd --no-create-home --uid 10001 app && chmod -R a+rX /app
USER app

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]