python
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

    @bp.route('/device-action', methods=['POST'])
    def device_action():
        data = request.get_json()
        device_identifier = data.get('deviceIdentifier')
        action = data.get('action')
        duration = data.get('duration', 0)

        try:
            result = device_service.send_action_to_device(device_identifier, action, duration)
            return jsonify({"status": "sent", "iot_response": result}), 200
        except Exception as e:
            logging.error(f"Error enviando acción al IoT: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return bp