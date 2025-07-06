# Multi-stage build for Railway deployment
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./

# Install dependencies (handle missing package-lock.json)
RUN if [ -f package-lock.json ]; then npm ci --only=production; else npm install --only=production; fi

COPY frontend/ ./
RUN npm run build

# Python backend stage with Alpine for smaller size
FROM python:3.11-alpine

WORKDIR /app

# Install system dependencies (minimal)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    nginx \
    && rm -rf /var/cache/apk/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build /app/static

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Create startup script
RUN echo '#!/bin/sh\n\
nginx &\n\
uvicorn main:app --host 0.0.0.0 --port 8000\n\
wait' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"] 