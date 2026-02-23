# Docker Documentation

Comprehensive Docker deployment guide for the Video Text Blur Tool and Web Application.

---

## Table of Contents

1. [Overview](#overview)
2. [Docker Components](#docker-components)
3. [Quick Start](#quick-start)
4. [Web Application Docker Setup](#web-application-docker-setup)
5. [API Server Docker Setup](#api-server-docker-setup)
6. [Docker Compose Orchestration](#docker-compose-orchestration)
7. [Configuration](#configuration)
8. [Networking](#networking)
9. [Volume Management](#volume-management)
10. [Production Deployment](#production-deployment)
11. [Troubleshooting](#troubleshooting)

---

## Overview

The project includes Docker configurations for two main components:

1. **VideoBluring WebApp**: Client-side web application with Nginx
2. **REST API Server**: Flask-based API for video processing (future)

### Benefits of Docker Deployment

- ✅ **Consistent Environment**: Same setup across development and production
- ✅ **Easy Deployment**: Single command to start services
- ✅ **Isolation**: Services run in isolated containers
- ✅ **Scalability**: Easy to scale horizontally
- ✅ **Portability**: Run anywhere Docker is supported

---

## Docker Components

### 1. VideoBluring WebApp

**Location**: `VideoBluring WebApp/Docker/`

**Components**:
- `Dockerfile` - Multi-stage build for web application
- `docker-compose.yml` - Orchestration configuration
- `nginx.conf` - Nginx server configuration
- `.dockerignore` - Build context exclusions
- `.env.example` - Environment variables template

**Base Image**: `nginx:1.25-alpine`

**Exposed Ports**: 8080 (production), 8081 (development)

### 2. REST API Server (Future)

**Location**: `swagger/` (Docker configuration to be added)

**Planned Components**:
- API server container
- Worker container for video processing
- Redis for job queue
- PostgreSQL for job storage

---

## Quick Start

### Prerequisites

- Docker Engine 20.10+ or Docker Desktop
- Docker Compose 2.0+
- 100MB free disk space
- Port 8080 available

### Start Web Application

```bash
# Navigate to Docker directory
cd "VideoBluring WebApp/Docker"

# Build and start
docker-compose up -d

# Access application
open http://localhost:8080
```

### Stop Application

```bash
docker-compose down
```

---

## Web Application Docker Setup

### Directory Structure

```
VideoBluring WebApp/
├── index.html
├── styles.css
├── script.js
├── README.md
└── Docker/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── nginx.conf
    ├── .dockerignore
    ├── .env.example
    └── README.md
```

### Dockerfile Explained

The Dockerfile uses a multi-stage build:

```dockerfile
# Stage 1: Builder (for future build steps)
FROM node:18-alpine AS builder
WORKDIR /app
COPY index.html styles.css script.js README.md ./

# Stage 2: Production with Nginx
FROM nginx:1.25-alpine AS production
RUN apk add --no-cache curl
RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY Docker/nginx.conf /etc/nginx/conf.d/default.conf

# Copy application files
COPY --from=builder /app/ /usr/share/nginx/html/

# Set permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
```

**Key Features**:
- Multi-stage build for optimization
- Custom Nginx configuration
- Health check endpoint
- Non-root user execution
- Minimal Alpine base image

### Building the Image

```bash
# From Docker directory
cd "VideoBluring WebApp/Docker"

# Build with default tag
docker build -t videobluring-webapp:latest -f Dockerfile ..

# Build with custom tag
docker build -t videobluring-webapp:v1.0.0 -f Dockerfile ..

# Build with no cache
docker build --no-cache -t videobluring-webapp:latest -f Dockerfile ..
```

### Running the Container

**Basic Run**:
```bash
docker run -d \
  --name videobluring-webapp \
  -p 8080:80 \
  videobluring-webapp:latest
```

**With Custom Port**:
```bash
docker run -d \
  --name videobluring-webapp \
  -p 3000:80 \
  videobluring-webapp:latest
```

**With Environment Variables**:
```bash
docker run -d \
  --name videobluring-webapp \
  -p 8080:80 \
  -e NGINX_HOST=example.com \
  videobluring-webapp:latest
```

### Nginx Configuration

The `nginx.conf` file provides:

**Security Headers**:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;" always;
```

**Compression**:
```nginx
gzip on;
gzip_comp_level 6;
gzip_types text/plain text/css text/javascript application/json;
```

**Caching**:
```nginx
# Static assets - 1 year cache
location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# HTML - no cache
location / {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

**Health Check**:
```nginx
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

---

## Docker Compose Orchestration

### docker-compose.yml Overview

```yaml
version: '3.8'

services:
  # Production service
  videobluring-webapp:
    build:
      context: ..
      dockerfile: Docker/Dockerfile
    container_name: videobluring-webapp-prod
    ports:
      - "${APP_PORT:-8080}:80"
    environment:
      - NGINX_HOST=${NGINX_HOST:-localhost}
    restart: unless-stopped
    networks:
      - webapp-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Development service with live reload
  videobluring-webapp-dev:
    image: nginx:1.25-alpine
    container_name: videobluring-webapp-dev
    ports:
      - "${DEV_PORT:-8081}:80"
    volumes:
      - ../index.html:/usr/share/nginx/html/index.html:ro
      - ../styles.css:/usr/share/nginx/html/styles.css:ro
      - ../script.js:/usr/share/nginx/html/script.js:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    profiles:
      - development

networks:
  webapp-network:
    driver: bridge

volumes:
  nginx-cache:
    driver: local
```

### Deployment Modes

**Production Mode** (default):
```bash
docker-compose up -d
# Runs on port 8080
```

**Development Mode** (with live reload):
```bash
docker-compose --profile development up -d videobluring-webapp-dev
# Runs on port 8081
# File changes reflect immediately
```

**With Reverse Proxy**:
```bash
docker-compose --profile proxy up -d
# Includes nginx-proxy for SSL/TLS
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Scale services
docker-compose up -d --scale videobluring-webapp=3

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

---

## Configuration

### Environment Variables

Create `.env` file in Docker directory:

```env
# Application Configuration
APP_PORT=8080
DEV_PORT=8081

# Nginx Configuration
NGINX_HOST=localhost
NGINX_PORT=80

# Proxy Configuration (if using proxy profile)
PROXY_HTTP_PORT=80
PROXY_HTTPS_PORT=443

# Logging
LOG_LEVEL=info
```

### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | 8080 | External port for production |
| `DEV_PORT` | 8081 | External port for development |
| `NGINX_HOST` | localhost | Server hostname |
| `NGINX_PORT` | 80 | Internal Nginx port |
| `PROXY_HTTP_PORT` | 80 | Reverse proxy HTTP port |
| `PROXY_HTTPS_PORT` | 443 | Reverse proxy HTTPS port |

### Using Environment Variables

```bash
# Set via command line
APP_PORT=3000 docker-compose up -d

# Set via .env file
echo "APP_PORT=3000" > .env
docker-compose up -d

# Set via export
export APP_PORT=3000
docker-compose up -d
```

---

## Networking

### Network Architecture

```
┌─────────────────────────────────────────┐
│           Host Machine                   │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Docker Network Bridge          │ │
│  │     (webapp-network)               │ │
│  │                                    │ │
│  │  ┌──────────────────────────────┐ │ │
│  │  │  videobluring-webapp-prod    │ │ │
│  │  │  Port: 80 → 8080             │ │ │
│  │  └──────────────────────────────┘ │ │
│  │                                    │ │
│  │  ┌──────────────────────────────┐ │ │
│  │  │  videobluring-webapp-dev     │ │ │
│  │  │  Port: 80 → 8081             │ │ │
│  │  └──────────────────────────────┘ │ │
│  │                                    │ │
│  │  ┌──────────────────────────────┐ │ │
│  │  │  nginx-proxy (optional)      │ │ │
│  │  │  Ports: 80, 443              │ │ │
│  │  └──────────────────────────────┘ │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Port Mapping

| Service | Internal Port | External Port | Protocol |
|---------|--------------|---------------|----------|
| Production | 80 | 8080 | HTTP |
| Development | 80 | 8081 | HTTP |
| Proxy HTTP | 80 | 80 | HTTP |
| Proxy HTTPS | 443 | 443 | HTTPS |

### Custom Network Configuration

```yaml
networks:
  webapp-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

### Container Communication

```bash
# Containers can communicate using service names
curl http://videobluring-webapp-prod/health

# From host machine
curl http://localhost:8080/health
```

---

## Volume Management

### Volume Types

**Named Volumes** (persistent):
```yaml
volumes:
  nginx-cache:
    driver: local
```

**Bind Mounts** (development):
```yaml
volumes:
  - ../index.html:/usr/share/nginx/html/index.html:ro
```

### Volume Commands

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect videobluring-nginx-cache

# Remove volume
docker volume rm videobluring-nginx-cache

# Remove all unused volumes
docker volume prune
```

### Backup and Restore

**Backup Volume**:
```bash
# Create backup
docker run --rm \
  -v videobluring-nginx-cache:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/nginx-cache-backup.tar.gz /data
```

**Restore Volume**:
```bash
# Restore from backup
docker run --rm \
  -v videobluring-nginx-cache:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/nginx-cache-backup.tar.gz -C /
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Update environment variables
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Review security settings
- [ ] Test health checks
- [ ] Configure firewall rules
- [ ] Set up reverse proxy (if needed)

### Production Configuration

**1. Use Production WSGI Server** (for API):
```dockerfile
# Install gunicorn
RUN pip install gunicorn

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "api_server:app"]
```

**2. Enable SSL/TLS**:
```yaml
services:
  nginx-proxy:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
      - ./nginx-proxy.conf:/etc/nginx/nginx.conf:ro
```

**3. Resource Limits**:
```yaml
services:
  videobluring-webapp:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
```

**4. Health Checks**:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

**5. Logging**:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
    labels: "production"
```

### Deployment Steps

```bash
# 1. Pull latest code
git pull origin main

# 2. Build images
docker-compose build --no-cache

# 3. Stop old containers
docker-compose down

# 4. Start new containers
docker-compose up -d

# 5. Verify deployment
docker-compose ps
curl http://localhost:8080/health

# 6. Check logs
docker-compose logs -f --tail=100
```

### Rolling Updates

```bash
# Build new version
docker build -t videobluring-webapp:v2.0.0 -f Dockerfile ..

# Tag as latest
docker tag videobluring-webapp:v2.0.0 videobluring-webapp:latest

# Update running container
docker-compose up -d --no-deps --build videobluring-webapp
```

### Blue-Green Deployment

```bash
# Start green deployment
docker-compose -f docker-compose.green.yml up -d

# Test green deployment
curl http://localhost:8082/health

# Switch traffic (update load balancer)
# ...

# Stop blue deployment
docker-compose -f docker-compose.blue.yml down
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solution**:
```bash
# Find process using port
lsof -i :8080

# Use different port
APP_PORT=8090 docker-compose up -d

# Or stop conflicting service
docker stop $(docker ps -q --filter "publish=8080")
```

#### 2. Container Won't Start

**Check logs**:
```bash
docker-compose logs videobluring-webapp

# Or
docker logs videobluring-webapp-prod
```

**Check container status**:
```bash
docker ps -a | grep videobluring
docker inspect videobluring-webapp-prod
```

#### 3. Permission Denied

**Error**: `Permission denied` when accessing files

**Solution**:
```bash
# Fix file permissions
chmod -R 755 ../

# Rebuild image
docker-compose build --no-cache
```

#### 4. Health Check Failing

**Check health status**:
```bash
docker inspect --format='{{json .State.Health}}' videobluring-webapp-prod | jq
```

**Test health endpoint**:
```bash
docker exec videobluring-webapp-prod curl http://localhost/health
```

#### 5. Image Build Fails

**Clear build cache**:
```bash
docker builder prune -a

# Rebuild
docker-compose build --no-cache --pull
```

#### 6. Cannot Access Application

**Check if container is running**:
```bash
docker ps | grep videobluring
```

**Check port mapping**:
```bash
docker port videobluring-webapp-prod
```

**Test from inside container**:
```bash
docker exec videobluring-webapp-prod curl http://localhost/
```

**Check firewall**:
```bash
# macOS
sudo pfctl -s rules

# Linux
sudo iptables -L
```

### Debug Mode

**Run with debug output**:
```bash
docker-compose up --verbose
```

**Interactive shell**:
```bash
docker exec -it videobluring-webapp-prod sh
```

**View Nginx logs**:
```bash
docker exec videobluring-webapp-prod cat /var/log/nginx/access.log
docker exec videobluring-webapp-prod cat /var/log/nginx/error.log
```

---

## Monitoring and Maintenance

### Container Stats

```bash
# Real-time stats
docker stats videobluring-webapp-prod

# One-time stats
docker stats --no-stream
```

### Log Management

```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs videobluring-webapp

# With timestamps
docker-compose logs -t
```

### Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything
docker system prune -a --volumes
```

---

## Security Best Practices

### 1. Use Non-Root User

```dockerfile
# Already implemented in Dockerfile
RUN chown -R nginx:nginx /usr/share/nginx/html
USER nginx
```

### 2. Scan for Vulnerabilities

```bash
# Using Docker scan
docker scan videobluring-webapp:latest

# Using Trivy
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image videobluring-webapp:latest
```

### 3. Keep Images Updated

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest
docker-compose build --no-cache
```

### 4. Use Secrets Management

```yaml
secrets:
  api_key:
    file: ./secrets/api_key.txt

services:
  videobluring-webapp:
    secrets:
      - api_key
```

### 5. Network Isolation

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

---

## See Also

- [VideoBluring WebApp/Docker/README.md](../VideoBluring%20WebApp/Docker/README.md) - Detailed Docker setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [Docker Documentation](https://docs.docker.com/) - Official Docker docs
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Compose reference

---

**Document Version**: 1.0.0  
**Last Updated**: February 23, 2026  
**Docker Version**: 20.10+  
**Docker Compose Version**: 2.0+

---

**End of Docker Documentation**