# Use Python 3.11 image instead of 3.12
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    git \
    make \
    cmake \
    unzip \
    wget \
    python3-dev \
    postgresql-client \
    libpq-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install dependencies in specific order
RUN pip install --no-cache-dir torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir numpy==1.26.3 scipy==1.11.4 nltk==3.8.1
RUN pip install --no-cache-dir scikit-learn==1.4.0
RUN pip install --no-cache-dir transformers==4.37.2 tokenizers==0.15.2 tqdm==4.66.2 huggingface-hub==0.20.3
RUN pip install --no-cache-dir sentence-transformers==2.2.2

# Install remaining ML dependencies
RUN pip install --no-cache-dir \
    safetensors==0.4.2 \
    accelerate==0.27.2

# Copy requirements and install remaining packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/chroma_db

# Install LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=true

# Run application
CMD ["uvicorn", "src.app_module:http_server", "--host", "0.0.0.0", "--port", "8000", "--reload"]