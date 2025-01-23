FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including ffmpeg and git
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and install GigaAM with verification
RUN git clone https://github.com/salute-developers/GigaAM.git && \
    cd GigaAM && \
    pip install . && \
    python3 -c "import gigaam; print('GigaAM successfully installed')" && \
    cd .. && \
    rm -rf GigaAM

# install pyannote.audio
RUN pip install pyannote.audio

# install model
COPY ./app/install_model.py .
RUN python3 /app/install_model.py

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Environment variable for the Hugging Face token
ENV HF_TOKEN="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"
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose the port the app runs on
EXPOSE 1488

# Use a shell form to ensure environment variables are available
CMD ["python3", "giga_api.py"]
