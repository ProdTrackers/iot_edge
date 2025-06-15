class Device:
    def __init__(self, device_identifier, latitude, longitude, inventory_id):
        self.device_identifier = device_identifier
        self.latitude = latitude
        self.longitude = longitude
        self.inventory_id = inventory_id

    def is_valid(self, valid_identifiers):
        return self.device_identifier in valid_identifiers