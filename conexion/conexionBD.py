import mysql.connector

def connectionBD_railway():
    try:
        connection = mysql.connector.connect(
            host="viaduct.proxy.rlwy.net",
            user="root",
            passwd="JWMQuXLFTTdFinFiKswjdeXhscBqmAtg",
            database="crud_python",
            port=24048,
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")


def connectionBD_invxx():
    try:
        connection = mysql.connector.connect(
            host="94.74.75.248",
            user="rpa_inventario_2",
            passwd="mIh23A7EB3yE5A3uXApOgEwOFOkI68",
            database="bd_claro",
            port=3306,
            charset='utf8',
            collation='utf8mb4_general_ci',
            raise_on_warnings=True
        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")

def connectionBD_inv():
    charsets = ['utf8mb4', 'utf8']  # Lista de charset a probar

    for charset in charsets:
        try:
            connection = mysql.connector.connect(
                host="94.74.75.248",
                user="rpa_inventario_2",
                passwd="mIh23A7EB3yE5A3uXApOgEwOFOkI68",
                database="bd_claro",
                port=3306,
                charset=charset,
                raise_on_warnings=True
            )
            if connection.is_connected():
                #print(f"Conectado con charset: {charset}")
                return connection

        except mysql.connector.Error as error:
            print(f"Fallo con charset {charset}: {error}")

    print("No se pudo conectar a la base de datos.")
    return None