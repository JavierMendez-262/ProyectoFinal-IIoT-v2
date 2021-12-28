import paho.mqtt.subscribe as subscribe
import json
import quality
from datetime import datetime


# Subscriber

# Función que recibe un mensaje de un publicador.
def received_message():
    # Se realiza una suscripción simple al tópico "home/livingRoom/table".
    message = subscribe.simple("home/livingRoom/table", hostname="192.168.0.30")
    # Se imprime el mensaje en consola.
    print(f"Sensor = {message.payload}")

    # Se transforma el json a dict
    sensor_data = json.loads(message.payload)
    sensor_data['datetime'] = datetime.now().strftime('%d-%b-%Y %H:%M:%S')

    quality.check_data(sensor_data)


while True:
    received_message()