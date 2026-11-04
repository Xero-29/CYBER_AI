from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint público seguro (sin cabeceras de metadatos sensibles)
@app.route('/api/v1/status', methods=['GET'])
def status():
    response = jsonify({
        "status": "online",
        "service": "internal-auth-gateway",
        "environment": "production"
    })
    
    # Eliminamos deliberadamente la exposición de cabeceras internas y versiones exactas.
    # Solo devolvemos lo estrictamente necesario.
    response.headers['Server'] = 'SecureGateway'
    return response, 200

# Endpoint protegido simulado
@app.route('/api/v1/admin/config', methods=['GET'])
def admin_config():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized", "message": "Missing or invalid token"}), 401
    return jsonify({"config": "secret_internal_parameters_secured"}), 200

if __name__ == '__main__':
    print("=== INICIANDO API SEGURA EN http://127.0.0.1:5000 ===")
    app.run(host='127.0.0.1', port=5000, debug=False)
