from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
from turl import TARGET_URL
import mimetypes

app = Flask(__name__, static_folder=None)
CORS(app)

TARGET_URL = TARGET_URL

# Ensure proper MIME types are registered
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/x-icon', '.ico')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # Construct the target URL
    target = f"{TARGET_URL}/{path}"
    
    # Forward the request headers
    headers = {key: value for key, value in request.headers if key.lower() not in ['host', 'content-length']}
    
    # Add Accept header for CSS files
    if path.endswith('.css'):
        headers['Accept'] = 'text/css'
    elif path.endswith('.ico'):
        headers['Accept'] = 'image/x-icon'
    
    try:
        # Forward the request with the same method and data
        response = requests.request(
            method=request.method,
            url=target,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            params=request.args,
            allow_redirects=False
        )
        
        # Create Flask Response object
        proxy_response = Response(
            response.content,
            status=response.status_code
        )
        
        # Forward ALL response headers except a select few
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        
        # Copy all headers from the original response
        for name, value in response.headers.items():
            if name.lower() not in excluded_headers:
                proxy_response.headers[name] = value
        
        # Ensure proper content type for static files
        if path.endswith('.css'):
            proxy_response.headers['Content-Type'] = 'text/css'
        elif path.endswith('.ico'):
            proxy_response.headers['Content-Type'] = 'image/x-icon'
            
        # Add CORS headers for static files
        if path.endswith(('.css', '.ico', '.js')):
            proxy_response.headers['Access-Control-Allow-Origin'] = '*'
        
        return proxy_response
        
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting proxy server on http://localhost:8080")
    print(f"Proxying requests to {TARGET_URL}")
    app.run(host='0.0.0.0', port=8080, debug=True)
