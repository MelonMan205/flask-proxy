FROM nginx:alpine

# Install required packages
RUN apk add --no-cache gettext curl

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our Nginx config
COPY nginx.conf /etc/nginx/nginx.template



# Use environment variable in nginx.conf and start nginx
CMD ["/bin/sh", "-c", "envsubst '${TARGET_URL}' < /etc/nginx/nginx.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]

# Expose port 8080 for Cloud Run
EXPOSE 8080 
