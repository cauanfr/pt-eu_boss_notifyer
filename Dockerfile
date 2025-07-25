FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Create and activate virtual environment
RUN python -m venv --copies /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install -r requirements.txt

# Create audios directory
RUN mkdir -p audios

# Copy your application
COPY . .

# Your application command
CMD ["python", "main.py"]