# Multi-stage Dockerfile for VideoBluring WebApp
# Stage 1: Build stage (for potential future build steps)
FROM node:18-alpine AS builder

WORKDIR /app

# Copy application files (context is parent directory)
COPY index.html ./
COPY styles.css ./
COPY script.js ./
COPY README.md ./

# Stage 2: Production stage with Nginx
FROM nginx:1.25-alpine AS production

# Install additional tools for debugging (optional)
RUN apk add --no-cache curl

# Remove default nginx configuration
RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration (from Docker subdirectory)
COPY Docker/nginx.conf /etc/nginx/conf.d/default.conf

# Copy application files from builder stage
COPY --from=builder /app/index.html /usr/share/nginx/html/
COPY --from=builder /app/styles.css /usr/share/nginx/html/
COPY --from=builder /app/script.js /usr/share/nginx/html/
COPY --from=builder /app/README.md /usr/share/nginx/html/

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Create nginx cache directories
RUN mkdir -p /var/cache/nginx/client_temp && \
    mkdir -p /var/cache/nginx/proxy_temp && \
    mkdir -p /var/cache/nginx/fastcgi_temp && \
    mkdir -p /var/cache/nginx/uwsgi_temp && \
    mkdir -p /var/cache/nginx/scgi_temp && \
    chown -R nginx:nginx /var/cache/nginx

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Expose port 8080
EXPOSE 8080

# Start nginx (run as root to avoid permission issues)
CMD ["nginx", "-g", "daemon off;"]