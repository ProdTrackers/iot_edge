from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("edge_server.log"),
        logging.StreamHandler()
    ]
)

# URL del backend real (Railway)
#BACKEND_URL = "https://backend-production-41be.up.railway.app/api/v1/iot-devices"

# URL del backend local
BACKEND_URL = "http://localhost:8000/api/v1/iot-devices"

# Lista de identificadores válidos (simulación de autenticidad)
VALID_DEVICE_IDENTIFIERS = {"esp32-001"}

@app.route('/device-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    logging.info(f"Datos recibidos del ESP32: {data}")

    # Validación de campos requeridos
    required_fields = {"latitude", "longitude", "deviceIdentifier", "inventoryId"}
    if not data or not required_fields.issubset(data):
        logging.warning("Faltan datos requeridos")
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Validación de autenticidad del dispositivo
    if data["deviceIdentifier"] not in VALID_DEVICE_IDENTIFIERS:
        logging.warning(f"Dispositivo no autorizado: {data['deviceIdentifier']}")
        return jsonify({"error": "Dispositivo no autorizado"}), 403

    # Enviar al backend
    try:
        response = requests.post(BACKEND_URL, json=data, timeout=5)
        logging.info(f"Respuesta del backend: {response.status_code} - {response.text}")
        return jsonify({"status": "OK", "backendCode": response.status_code}), response.status_code
    except Exception as e:
        logging.error(f"Error al enviar al backend: {e}")
        return jsonify({"error": "Fallo al contactar el backend"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
