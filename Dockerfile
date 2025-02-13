FROM nginx:alpine

# Install envsubst
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf /etc/nginx/nginx.template

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Start nginx with environment variable substitution
CMD envsubst '${TARGET_URL}' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'

# Expose port 8080 for Cloud Run
EXPOSE 8080 
