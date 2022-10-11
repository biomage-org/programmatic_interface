FROM python:3.9.9-slim

# Install app dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt && \
    apt update && apt install -y procps && rm -rf /var/lib/apt/lists/*
