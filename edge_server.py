from flask import Flask
import logging
import os

from infrastructure.backend_client import BackendClient
from application.services import DeviceService
from interfaces.routes import create_routes

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("edge_server.log"),
        logging.StreamHandler()
    ]
)

BACKEND_URL = "https://backend-production-41be.up.railway.app/api/v1/iot-devices"
VALID_DEVICE_IDENTIFIERS = {"esp32-001"}

app = Flask(__name__)

# Inyección de dependencias
backend_client = BackendClient(BACKEND_URL)
device_service = DeviceService(backend_client, VALID_DEVICE_IDENTIFIERS)

# Registro de rutas
app.register_blueprint(create_routes(device_service))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
