from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
from turl import TARGET_URL

app = Flask(__name__, static_folder=None)
CORS(app)

TARGET_URL = TARGET_URL

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    # Construct the target URL
    target = f"{TARGET_URL}/{path}"
    
    # Forward the request headers
    headers = {key: value for key, value in request.headers if key != 'Host'}
    
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
        
        # Forward response headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.headers.items()
                  if name.lower() not in excluded_headers]
        
        # Preserve Content-Type header
        for header, value in headers:
            proxy_response.headers[header] = value
                
        return proxy_response
        
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting proxy server on http://localhost:8080")
    print(f"Proxying requests to {TARGET_URL}")
    app.run(host='0.0.0.0', port=8080, debug=True)