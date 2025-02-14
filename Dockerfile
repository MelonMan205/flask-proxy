FROM nginx:alpine

# Copy the custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose Cloud Run’s default port
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
