FROM python:3.11-slim

# Avoid prompts and set noninteractive mode
ENV DEBIAN_FRONTEND=noninteractive

# Ensure apt works with HTTPS and install required debug tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    iputils-ping \
    net-tools \
    dnsutils \
    vim \
    netcat-traditional \
    wget \
    bash \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app source and requirements
COPY . .

# Install Python dependencies including gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Expose Gunicorn port
EXPOSE 5008

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5008", "app:app"]
