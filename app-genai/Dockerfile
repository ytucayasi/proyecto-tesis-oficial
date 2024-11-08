# Use Python 3.12 image
FROM python:3.12-slim

# Update the package list and install essential tools
RUN apt-get update && \
    apt-get install -y \
    vim \
    telnet \
    inetutils-ping \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev

# Set the working directory inside the container
WORKDIR /app

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir pip==24.0

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Define the command to run the application
CMD ["uvicorn", "src.app_module:http_server", "--host", "0.0.0.0", "--port", "8000", "--reload"]