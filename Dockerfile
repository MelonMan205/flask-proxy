FROM nginx:alpine

# Install envsubst
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf /etc/nginx/nginx.template

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Create log directory and set permissions
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Start nginx with environment variable substitution
CMD envsubst '${TARGET_URL}' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'

# Expose port 8080 for Cloud Run
EXPOSE 8080 
