import pymongo


# Database
class Database:

    # Constructor que inicializa la base de datos
    def __init__(self):
        # Se realiza la conexión al host de la base de datos
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        # Se establece la base de datos a la cual realizar los querys
        self.db = client["sensorsdatabase"]

    # Registra un elemento dict en la base de datos
    def insert_dict(self, dict, col_name):
        # Se establece el nombre de la coleccion a ingresar datos
        col = self.db[col_name]

        # Se insertan los datos
        col.insert_one(dict)

    def get_dict(self, col_name, quantity=1):
        # Se establece el nombre de la coleccion a ingresar datos
        col = self.db[col_name]

        return col.find().limit(quantity).sort([("$natural", pymongo.DESCENDING)])

    # Obtiene los ultimos conjuntos de datos ingresados a la base de datos
    def get_sensor_dataset(self, id, is_temperature, quantity=1):
        col_name = 'sensorsdata'
        # Se establece el nombre de la coleccion a ingresar datos
        col = self.db[col_name]

        # Obtiene los ultimos x (x = quantity) conjuntos de datos ingresados a la base de datos con el id del parametro
        raw_dataset = col.find({"id": id}).limit(quantity).sort([("$natural", pymongo.DESCENDING)])

        # Se almacenan en una lista
        dataset = []
        for data in raw_dataset:
            dataset.append(data["temperature" if is_temperature else "humidity"])

        # Regresa la lista
        return dataset

    # Regresa las fechas
    def get_datetime_dataset(self, id, quantity=1):
        col_name = 'sensorsdata'
        # Se establece el nombre de la coleccion a ingresar datos
        col = self.db[col_name]

        # Obtiene los ultimos x (x = quantity) conjuntos de datos ingresados a la base de datos con el id del parametro
        raw_dataset = col.find({"id": id}).limit(quantity).sort([("$natural", pymongo.DESCENDING)])

        # Se almacenan en una lista
        dataset = []
        for data in raw_dataset:
            dataset.append(data["datetime"])

        # Regresa la lista
        return dataset