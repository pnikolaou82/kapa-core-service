FROM python:3.11-slim

# Avoid prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Install common debugging tools
RUN apt-get update && apt-get install -y \
    curl \
    iproute2 \
    iputils-ping \
    net-tools \
    dnsutils \
    vim \
    netcat \
    wget \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code and install dependencies
COPY . .

# Install Python dependencies + gunicorn
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install gunicorn

# Expose the port used by Gunicorn
EXPOSE 5008

# Run Gunicorn instead of Flask's dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5008", "app:app"]
