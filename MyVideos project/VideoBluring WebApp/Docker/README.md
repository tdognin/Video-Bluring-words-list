# Docker Setup for VideoBluring WebApp

Complete Docker configuration for deploying the VideoBluring WebApp with Nginx in containerized environments.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment Modes](#deployment-modes)
- [Environment Variables](#environment-variables)
- [Building Images](#building-images)
- [Running Containers](#running-containers)
- [Volume Management](#volume-management)
- [Port Mapping](#port-mapping)
- [Health Checks](#health-checks)
- [Logging](#logging)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

## 🎯 Overview

This Docker setup provides:
- **Multi-stage Dockerfile** for optimized image size
- **Docker Compose** orchestration for easy deployment
- **Nginx** web server with optimized caching and compression
- **Development and Production** configurations
- **Health checks** and monitoring
- **Security hardening** with non-root user

## 📦 Prerequisites

- Docker Engine 20.10+ or Docker Desktop
- Docker Compose 2.0+
- 100MB free disk space
- Port 8080 available (or configure custom port)

## 🚀 Quick Start

### 1. Navigate to Docker Directory

```bash
cd "VideoBluring WebApp/Docker"
```

### 2. Build and Run (Production)

```bash
# Build and start the container
docker-compose up -d

# Access the application
open http://localhost:8080
```

### 3. Stop the Application

```bash
docker-compose down
```

## ⚙️ Configuration

### File Structure

```
Docker/
├── Dockerfile              # Multi-stage build configuration
├── docker-compose.yml      # Orchestration configuration
├── nginx.conf             # Nginx server configuration
├── .dockerignore          # Build context exclusions
└── README.md              # This file
```

## 🎭 Deployment Modes

### Production Mode (Default)

Optimized for production with built image:

```bash
docker-compose up -d
```

Features:
- Optimized Nginx configuration
- Gzip compression enabled
- Static asset caching
- Security headers
- Health checks

### Development Mode

Live reload with volume mounting:

```bash
docker-compose --profile development up -d videobluring-webapp-dev
```

Features:
- Hot reload on file changes
- Direct file mounting
- Faster iteration
- Runs on port 8081

### With Reverse Proxy

For SSL/TLS termination and advanced routing:

```bash
docker-compose --profile proxy up -d
```

## 🔧 Environment Variables

Create a `.env` file in the Docker directory:

```env
# Application Port
APP_PORT=8080

# Development Port
DEV_PORT=8081

# Nginx Configuration
NGINX_HOST=localhost
NGINX_PORT=80

# Proxy Configuration (if using proxy profile)
PROXY_HTTP_PORT=80
PROXY_HTTPS_PORT=443
```

### Default Values

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | 8080 | External port for production |
| `DEV_PORT` | 8081 | External port for development |
| `NGINX_HOST` | localhost | Server hostname |
| `NGINX_PORT` | 80 | Internal Nginx port |

## 🏗️ Building Images

### Build Production Image

```bash
# From Docker directory
docker build -t videobluring-webapp:latest -f Dockerfile ..

# Or using docker-compose
docker-compose build
```

### Build with Custom Tag

```bash
docker build -t videobluring-webapp:v1.0.0 -f Dockerfile ..
```

### Build Arguments (if needed)

```bash
docker build \
  --build-arg NODE_VERSION=18 \
  -t videobluring-webapp:latest \
  -f Dockerfile ..
```

## 🏃 Running Containers

### Using Docker Compose (Recommended)

```bash
# Start in background
docker-compose up -d

# Start with logs
docker-compose up

# Start specific service
docker-compose up -d videobluring-webapp

# Scale (if needed)
docker-compose up -d --scale videobluring-webapp=3
```

### Using Docker CLI

```bash
# Run production container
docker run -d \
  --name videobluring-webapp \
  -p 8080:80 \
  --restart unless-stopped \
  videobluring-webapp:latest

# Run with custom port
docker run -d \
  --name videobluring-webapp \
  -p 3000:80 \
  videobluring-webapp:latest
```

### Development with Volume Mounting

```bash
docker run -d \
  --name videobluring-webapp-dev \
  -p 8081:80 \
  -v "$(pwd)/../index.html:/usr/share/nginx/html/index.html:ro" \
  -v "$(pwd)/../styles.css:/usr/share/nginx/html/styles.css:ro" \
  -v "$(pwd)/../script.js:/usr/share/nginx/html/script.js:ro" \
  -v "$(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf:ro" \
  nginx:1.25-alpine
```

## 💾 Volume Management

### List Volumes

```bash
docker volume ls | grep videobluring
```

### Inspect Volume

```bash
docker volume inspect videobluring-nginx-cache
```

### Remove Volumes

```bash
# Remove all project volumes
docker-compose down -v

# Remove specific volume
docker volume rm videobluring-nginx-cache
```

## 🔌 Port Mapping

### Default Ports

| Service | Internal Port | External Port | Description |
|---------|--------------|---------------|-------------|
| Production | 80 | 8080 | Main application |
| Development | 80 | 8081 | Dev environment |
| Proxy HTTP | 80 | 80 | Reverse proxy |
| Proxy HTTPS | 443 | 443 | SSL/TLS proxy |

### Custom Port Configuration

Edit `docker-compose.yml` or use environment variables:

```bash
APP_PORT=3000 docker-compose up -d
```

## 🏥 Health Checks

### Container Health Status

```bash
# Check health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Detailed health check
docker inspect --format='{{json .State.Health}}' videobluring-webapp-prod | jq
```

### Manual Health Check

```bash
# HTTP health check
curl http://localhost:8080/health

# Expected response: "healthy"
```

### Health Check Configuration

Located in `docker-compose.yml`:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 10 seconds

## 📊 Logging

### View Logs

```bash
# All services
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs videobluring-webapp

# Last 100 lines
docker-compose logs --tail=100

# With timestamps
docker-compose logs -t
```

### Log Configuration

Logs are configured with JSON file driver:
- Max size: 10MB (production), 5MB (development)
- Max files: 3 (production), 2 (development)

### Access Nginx Logs

```bash
# Access logs
docker exec videobluring-webapp-prod cat /var/log/nginx/access.log

# Error logs
docker exec videobluring-webapp-prod cat /var/log/nginx/error.log
```

## 🔒 Security

### Security Features

1. **Non-root User**: Container runs as `nginx` user
2. **Security Headers**: X-Frame-Options, X-Content-Type-Options, CSP
3. **Read-only Volumes**: Mounted files are read-only
4. **Minimal Base Image**: Alpine Linux for reduced attack surface
5. **No Sensitive Data**: All processing is client-side

### Security Best Practices

```bash
# Scan image for vulnerabilities
docker scan videobluring-webapp:latest

# Run security audit
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image videobluring-webapp:latest
```

### Update Base Images

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest
docker-compose build --no-cache
```

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs videobluring-webapp

# Check container status
docker ps -a | grep videobluring

# Inspect container
docker inspect videobluring-webapp-prod
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8080

# Use different port
APP_PORT=8090 docker-compose up -d
```

### Permission Issues

```bash
# Fix file permissions
chmod -R 755 ../

# Rebuild image
docker-compose build --no-cache
```

### Image Build Fails

```bash
# Clean build cache
docker builder prune -a

# Rebuild from scratch
docker-compose build --no-cache --pull
```

### Application Not Accessible

```bash
# Check if container is running
docker ps | grep videobluring

# Check port mapping
docker port videobluring-webapp-prod

# Test from inside container
docker exec videobluring-webapp-prod curl http://localhost/
```

## 🚀 Production Deployment

### Pre-deployment Checklist

- [ ] Update environment variables
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Review security settings
- [ ] Test health checks
- [ ] Configure firewall rules

### Deploy to Production

```bash
# Pull latest code
git pull origin main

# Build production image
docker-compose build

# Stop old container
docker-compose down

# Start new container
docker-compose up -d

# Verify deployment
curl http://localhost:8080/health
```

### With SSL/TLS (Using Reverse Proxy)

1. Place SSL certificates in `ssl/` directory:
   ```
   ssl/
   ├── certificate.crt
   └── private.key
   ```

2. Create `nginx-proxy.conf` with SSL configuration

3. Start with proxy profile:
   ```bash
   docker-compose --profile proxy up -d
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

### Backup and Restore

```bash
# Backup image
docker save videobluring-webapp:latest | gzip > videobluring-webapp-backup.tar.gz

# Restore image
docker load < videobluring-webapp-backup.tar.gz
```

## 📈 Monitoring

### Container Stats

```bash
# Real-time stats
docker stats videobluring-webapp-prod

# One-time stats
docker stats --no-stream
```

### Resource Limits

Add to `docker-compose.yml`:

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

## 🧹 Cleanup

### Remove Containers

```bash
# Stop and remove containers
docker-compose down

# Remove with volumes
docker-compose down -v

# Remove with images
docker-compose down --rmi all
```

### Clean Docker System

```bash
# Remove unused containers, networks, images
docker system prune

# Remove everything (careful!)
docker system prune -a --volumes
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

## 🆘 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Docker logs: `docker-compose logs`
3. Check container health: `docker ps`
4. Verify configuration files

## 📝 License

This Docker configuration is part of the VideoBluring WebApp project.

---

**Last Updated**: 2026-02-22  
**Docker Version**: 20.10+  
**Docker Compose Version**: 2.0+