import notificator
from database import Database
import math
import json


# Quality

# Verifica la calidad de los datos
def check_data(sensor_data):
    # Se construye un objeto Database
    db = Database()

    # Si los datos recolectados son mayores a 5 se validan
    if len(db.get_sensor_dataset(sensor_data['id'], is_temperature=True)) >= query_qty:

        # Se obtienen un conjunto de datos discriminados por los parametros
        dataset = db.get_sensor_dataset(sensor_data['id'], is_temperature=True, quantity=query_qty)
        # Promedio y Desv Estandar de la temperatura
        temp = __standard_desv(dataset)

        # Se obtienen un conjunto de datos discriminados por los parametros
        dataset = db.get_sensor_dataset(sensor_data['id'], is_temperature=False, quantity=query_qty)
        # Promedio y Desv Estandar de la humedad
        hum = __standard_desv(dataset)

        # Se establece una cantidad maxima de cambio de temperatura en una hora
        if (temp[1] < max_temp_change):
            temp = (temp[0], max_temp_change)
        # Se establece una cantidad maxima de cambio de humedad en una hora
        if (hum[1] < max_hum_change):
            hum = (hum[0], max_hum_change)

        # Si no son datos atipicos se guardan y se notifica de la informacion capturada por el sensor
        if temp[0] + temp[1] * 3 >= sensor_data['temperature'] >= temp[0] - temp[1] * 3:
            if hum[0] + hum[1] * 3 >= sensor_data['humidity'] >= hum[0] - hum[1] * 3:
                __save_data(sensor_data, db, 'sensorsdata')

                # Si la temperatura no se encuentra debajo del umbral permitido
                if not __under_threshold(sensor_data['temperature']):
                    # Se envia una alerta
                    __send_notification(sensor_data)
                    # Se guarda un registro de la alerta en la base de datos
                    __save_data(sensor_data, db, 'alertsdata')

                print('datos validados y almacenados!')
            else:
                print('datos atipicos')
        else:
            print('datos atipicos')
    # En caso contrario se registran para poder validar los posteriores
    else:
        print('obteniendo datos')
        __save_data(sensor_data, db, 'sensorsdata')

        # Si la temperatura no se encuentra debajo del umbral permitido
        if not __under_threshold(sensor_data['temperature']):
            # Se envia una alerta
            __send_notification(sensor_data)
            # Se guarda un registro de la alerta en la base de datos
            __save_data(sensor_data, db, 'alertsdata')

# Almacena la información en la base de datos
def __save_data(sensor_data, db, col_name):
    # Registra los datos
    db.insert_dict(sensor_data, col_name)

# Envía una notificación por correo electronico
def __send_notification(sensor_data):
    # Se le envian las lecturas del sensor a notificator.py para enviar una notificación al usuario
    notificator.notify(sensor_data)

# Calcula la desviación estándar a partir de una colección de números
def __standard_desv(num_col):
    summ = sum(num_col)
    prom = summ / len(num_col)

    summ = 0
    for x in num_col:
        summ += (x - prom) ** 2

    vrnce = summ / (len(num_col))
    desv = math.sqrt(vrnce)

    return prom, desv

# valida que la temperatura se encuentre dentro del umbral establecido
def __under_threshold(temperature):
    file = open('data.json',)
    data = json.load(file)
    file.close()
    return temperature < data['thresholds']['max_temperature']


# Variables
# Cantidad de consulta de datos para validar los datos
query_qty = 5
# Estas variables son utilizadas para marcar el valor maximo de cambio en un hora para la temperatura y humedad.
# Considerar que luego se multiplican por 3
max_temp_change = 1
max_hum_change = 2
