import requests
import logging

class BackendClient:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def send_to_backend(self, data):
        response = requests.post(self.backend_url, json=data, timeout=5)
        logging.info(f"Respuesta del backend: {response.status_code} - {response.text}")
        return response