FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Fetch Smuggler tool source
RUN git clone --depth 1 https://github.com/defparam/smuggler.git /opt/smuggler

# Copy application code
COPY . .

ENV HOST=0.0.0.0
ENV SMUGGLER_PATH=/opt/smuggler/smuggler.py
EXPOSE 8000

CMD ["python", "server.py"]
