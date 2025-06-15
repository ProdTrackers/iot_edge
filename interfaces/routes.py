from flask import Blueprint, request, jsonify
import logging

def create_routes(device_service):
    bp = Blueprint('routes', __name__)

    @bp.route('/device-data', methods=['POST'])
    def receive_data():
        data = request.get_json()
        logging.info(f"Datos recibidos del ESP32: {data}")
        response, status = device_service.process_device_data(data)
        return jsonify(response), status

    return bp