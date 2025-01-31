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
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
            raise_on_warnings=True

        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")

def connectionBD_inv():
    try:
        connection = mysql.connector.connect(
            host="94.74.75.248",
            user="rpa_inventario_2",
            passwd="mIh23A7EB3yE5A3uXApOgEwOFOkI68",
            database="bd_claro",
            port=3306,
            charset='utf8mb4',
            #collation='utf8mb4_general_ci',# Solo usa charset
            raise_on_warnings=True
        )
        if connection.is_connected():
            # Conexión exitosa
            #print(connection)
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None
