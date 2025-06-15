# IoT Edge Server

Este proyecto implementa un **IoT Edge** usando Python y Flask para recibir datos de dispositivos IoT (por ejemplo, ESP32 con GPS) y reenviarlos a un backend centralizado. Es ideal para escenarios de simulación, pruebas o despliegue en entornos edge.

## Características

- Recibe datos de ubicación (latitud, longitud) y metadatos de dispositivos IoT.
- Valida la autenticidad del dispositivo antes de reenviar la información.
- Reenvía los datos al backend principal (por ejemplo, una API en Java Spring Boot).
- Registro de logs para auditoría y depuración.
- Preparado para despliegue en Railway o servidores compatibles con Gunicorn.

## Estructura de archivos

```
iot-edge/
├── edge_server.py
├── requirements.txt
├── Procfile
└── README.md
```

## Instalación local

1. Clona el repositorio:
    ```
    git clone https://github.com/tu-usuario/iot-edge.git
    cd iot-edge
    ```

2. (Opcional) Crea y activa un entorno virtual:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```

4. Ejecuta el servidor:
    ```
    python edge_server.py
    ```

## Despliegue en Railway

1. Sube el proyecto a un repositorio en GitHub.
2. En Railway, crea un nuevo proyecto y selecciona tu repositorio.
3. Railway instalará automáticamente las dependencias y ejecutará el comando del `Procfile`.
4. Usa la URL pública que te da Railway para conectar tus dispositivos IoT.

## Uso

El servidor expone el endpoint:

```
POST /device-data
Content-Type: application/json

{
  "deviceIdentifier": "esp32-001",
  "latitude": 12.345678,
  "longitude": -98.765432,
  "inventoryId": 5
}
```

## Notas

- Modifica la lista `VALID_DEVICE_IDENTIFIERS` en `edge_server.py` para autorizar nuevos dispositivos.
- El backend debe estar accesible desde el servidor edge.
- Para producción, considera usar HTTPS y mejorar la autenticación.

---

Desarrollado para fines educativos y