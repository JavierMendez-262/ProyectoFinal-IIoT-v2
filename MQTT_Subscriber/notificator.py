import requests


# Email Notifications

# Envía una notificación a gmail con los datos capturados por el sensor
def notify(sensor_data):
    # API-endpoint
    url = 'https://maker.ifttt.com/trigger/esp32/with/key/T1NIWOM4WyIbGvzBL_DjUsn6qMZMkHRslWHCb0fzth'
    # Se definen los parámetros para ser enviados al API
    params = {'value1': sensor_data['id'], 'value2': sensor_data['temperature'], 'value3': sensor_data['humidity']}

    print('Alerta enviada!')
    # Se envía una solicitud POST al API junto con sus parámetros
    ###requests.post(url=url, params=params)

    