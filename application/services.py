from domain.device import Device

class DeviceService:
    def __init__(self, backend_client, valid_identifiers):
        self.backend_client = backend_client
        self.valid_identifiers = valid_identifiers

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