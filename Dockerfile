# Use official Python base image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install debugging tools and Postgres client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    iputils-ping \
    dnsutils \
    curl \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY start.sh .

RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
