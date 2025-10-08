FROM python:3.10-slim

# Install ffmpeg and system tools
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for cache efficiency)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Optional: expose port (for debugging)
EXPOSE 8000

# Run the handler
CMD ["python", "handler.py"]
