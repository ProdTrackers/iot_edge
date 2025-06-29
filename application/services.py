import requests
from domain.device import Device

class DeviceService:
    def __init__(self, backend_client, valid_identifiers, device_ip_map):
        self.backend_client = backend_client
        self.valid_identifiers = valid_identifiers
        self.device_ip_map = device_ip_map  # Diccionario: deviceIdentifier -> IP

    def process_device_data(self, data):
        required_fields = {"latitude", "longitude", "deviceIdentifier", "inventoryId"}
        if not data or not required_fields.issubset(data):
            return {"error": "Faltan datos requeridos"}, 400

        device = Device(
            data["deviceIdentifier"],
            data["latitude"],
            data["longitude"],
            data["inventoryId"]
        )

        if not device.is_valid(self.valid_identifiers):
            return {"error": "Dispositivo no autorizado"}, 403

        try:
            backend_response = self.backend_client.send_to_backend(data)
            return {
                "status": "OK",
                "backendCode": backend_response.status_code
            }, backend_response.status_code
        except Exception as e:
            return {"error": "Fallo al contactar el backend"}, 500

    def turn_on_led(self, device_identifier):
        # Busca la IP del dispositivo
        esp32_ip = self.device_ip_map.get(device_identifier)
        if not esp32_ip:
            return {"error": "Dispositivo no encontrado"}, 404

        iot_url = f"http://{esp32_ip}/led/on"
        try:
            resp = requests.post(iot_url, timeout=5)
            if resp.status_code == 200:
                return {"status": "LED encendido"}, 200
            else:
                return {"error": "Fallo al encender el LED"}, resp.status_code
        except Exception as e:
            return {"error": f"Error de conexión: {str(e)}"}, 500