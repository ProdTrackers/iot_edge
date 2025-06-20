import requests
import logging

class BackendClient:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def send_to_backend(self, data):
        response = requests.post(self.backend_url, json=data, timeout=5)
        logging.info(f"Respuesta del backend: {response.status_code} - {response.text}")
        return response

    def is_device_reserved(self, device_id):
        url = f"{self.backend_url}/{device_id}/is-reserved"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()  # True o False
        except Exception as e:
            logging.warning(f"No se pudo verificar si el dispositivo está reservado: {e}")
            return False  # asume que no está reservado si falla
