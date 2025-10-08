FROM python:3.10-slim

# Install system dependencies for OpenCV, Transparent Background, etc.
RUN apt-get update && \
    apt-get install -y git ffmpeg libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

EXPOSE 8000

CMD ["python", "handler.py"]
