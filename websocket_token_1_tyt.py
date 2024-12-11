import websocket
import json
import logging
from itertools import cycle
import mysql.connector
from datetime import datetime
import requests
import re
import socket
import os 
import inspect
import asyncio
from telegram.ext import Application
# Configuración básica del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("inicio del websocket")

credentials_bdd_claro={
    'host':'94.74.75.248',
    'database':'bd_claro',
    'user':'rpa_inventario_2',
    'password':'mIh23A7EB3yE5A3uXApOgEwOFOkI68',
}

credentials_log={
    'host':'94.74.75.248',
    'database':'bd_log',
    'user':'rpa_inventario_2',
    'password':'mIh23A7EB3yE5A3uXApOgEwOFOkI68',
}

claro_bdd_conn=None
numeros = cycle(range(0, 5))
errors=0
token = '7001689782:AAEvAcI3Y60x1Wa4mB1tncBhVlOO_W1m1hQ'
chat_id = '-1001839039241'

#Login bases de datos ----------------------------------------------------------------------------------------------------------------------

def DB_login(credentials):
    connection=None
    error=None
    try:
        connection = mysql.connector.connect(
            host=credentials['host'],
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
        )
        print("Conexión a MySQL DataWarehouse exitosa !!!")
    except Exception as e:
        error={str(inspect.currentframe().f_code.co_name):e}
        print(f"Error en logindb : {e}")
    finally:    
        return connection,error 

def upload_tokenBD(conn,token):
    with conn.cursor() as cursor:
        query="""
        INSERT INTO token_poliedro (token, tipo_token, campaing) VALUES( %s,'2','Claro TyT' )
        """
        values=(token,)
        cursor.execute(query, values)
        conn.commit()  # Confirmar la inserción
        print("Token insertado exitosamente")

def establecer_conexion(credentials):
    connection=None
    error=None
    connection = mysql.connector.connect(
            host=credentials['host'],
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
        )
    print(f"Conexión exitosa a {credentials['database']} en {credentials['host']} !!!")

    return connection


def error_handler(func):
    def wrapper(*args, **kwargs):
        result = None
        error = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            # Obtener el nombre de la función decorada
            function_name = func.__name__
            error = {str(function_name): str(e)}
            print(f"error en {error}")
        finally:
            # Si la función original devuelve algo, devolver el resultado y el error
            if result is not None:
                return result, error
            else:
                # Si no devuelve nada, devolver solo el error
                return error
    return wrapper


@error_handler
def subir_token_bdd(conn,token):
    if not conn:
        conn=establecer_conexion(credentials_bdd_claro)
    upload_tokenBD(conn,token)


def upload_log(connection, process, start_time, end_time, result, observation):
    error = None
    ip_address = socket.gethostbyname(socket.gethostname())
    try:
        #execution_time = end_time - start_time
        execution_time = (end_time - start_time).total_seconds()
        # Usar el cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            query = """
            INSERT INTO registro_ejecucion_procesos 
            (proceso, tiempo_ejecucion, resultado, observaciones,Fecha_inicio,Fecha_fin,IP_source) 
            VALUES ( %s, %s, %s, %s,%s,%s,%s)
            """
            values = (process, execution_time, result, observation,start_time,end_time,ip_address)
            cursor.execute(query, values)
            connection.commit()  # Confirmar la inserción
            print("Datos insertados exitosamente")
    except mysql.connector.Error as e:
        error = f"Error en la inserción de datos: {e}"
    except Exception as e:
        error = f"Error inesperado: {e}"
    finally:
        print(f"El error en upload_log es: {error}")
        return error


def enviar_gc(token,indice_lista):
  
    data = (
        "1728668239390x597560065347204600",
        "1728668243503x405728351194061060",
        "1728668248025x611165183096669100",
        "1728671871427x821675760174023700",
        "1728671876263x106562953036253970"
    ) 

    base_url = "https://goclient.bentoint.com/api/1.1/obj/token_poliedro"
    headers = {'Authorization': 'Bearer f03969f77c48f27e459b5fbf338eb086'}
    error=None
    try:
        token_elemento = data[indice_lista]
        url = base_url + "/" + token_elemento
        payload = {'Token': str(token)}

        response = requests.patch(url, headers=headers, data=payload)
        response.raise_for_status()
        logging.info(f"Actualización exitosa para el token en el indice {indice_lista}: {token_elemento} y su valor es {token}")
    except IndexError:
        error=f"El índice {indice_lista} está fuera del rango de la lista de tokens."
        logging.error(error)
        print(error)
    
    except requests.exceptions.RequestException as f:
        error=f"Hubo un problema con la solicitud para el token: {token_elemento} con indice {indice_lista}: {f}"
        logging.error(f"Hubo un problema con la solicitud para el token: {token_elemento} con indice {indice_lista}: {f}")
        print(error)
    finally:    
        return error 


#Login bases de datos ----------------------------------------------------------------------------------------------------------------------

#####Notificacion a telegram##########################################
async def send_message(error_msg):
    app = Application.builder().token(token).build()
    try:
        await app.bot.send_message(chat_id=chat_id, text=error_msg)
        print("Mensaje enviado a telegram exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al enviar el mensaje: {e}")


async def main(error_msg):
    await send_message(error_msg)


def send_telegram(errors):
    
    try:    
        errors_list = [e for e in errors if e is not None]
        print(f"el error list es {errors_list}")
        result="Success"
        if len(errors_list)>0:
            error_msg = f"Error en {os.path.basename(__file__)} : {errors_list}"
            asyncio.run(main(error_msg))
            print(error_msg)
            result="Error Sent"
            return errors_list,result
    except Exception as e:
        error={str(inspect.currentframe().f_code.co_name):str(e)}
        print(error)
        errors_list.append(error)
        result=f"No errors Sent "
        return errors_list,result
        
    finally:
        
        return str(errors_list),result

#####Notificacion a telegram##########################################


# Tu Access Token de Pushbullet claro
#ACCESS_TOKEN = "o.eVefl27l3Oxif6P2FaUn3y7k2T4AwI8E" # token jhon
ACCESS_TOKEN = "o.WHTjhu2e1n4sr6OQTHRQY3YjtWj2SwcS" #token 2 tyt
#ACCESS_TOKEN = "o.vHJSFuYaySaRBo6MEvo3TKUJAwGp5ZWw"

WS_URL = f"wss://stream.pushbullet.com/websocket/{ACCESS_TOKEN}"

start_time=datetime.now()

#\\10.4.11.19\bdinfo\Área DDBB\INTEGRANTES\JHON MORENO\Python

# Función que se ejecuta al recibir un mensaje del WebSocket
def on_message(ws, message):
    start_time=datetime.now()
    print("Mensaje recibido:")
    data = json.loads(message)  # Parsear el mensaje como JSON
    #print(f"el mensaje original es {data}")  # Imprimir el mensaje en formato legible
    print(f"el mensaje es {json.dumps(data, indent=4)}")  # Imprimir el mensaje en formato legible
    print(f" el type es  {data['type']}" )
    if data["type"]=="push":
        if "notifications" in data["push"]:
            if "body" in data["push"]["notifications"][0]:
                mensaje=data["push"]["notifications"][0]["body"]
                token=re.search(r'\d{8}', mensaje)
                if token:
                    #e22=enviar_gc(token.group(),next(numeros))
                    e2=subir_token_bdd(claro_bdd_conn,token.group())

    execution_time = (datetime.now() - start_time).total_seconds()
    print(f"el tiempo de ejecucion es {execution_time}")
# Función que se ejecuta cuando el WebSocket se abre
def on_open(ws):
    global start_time
    start_time=datetime.now()
    print("Conexión al WebSocket abierta.")
# Función que se ejecuta al cerrar el WebSocket
def on_close(ws, close_status_code, close_msg):
    global start_time
    start_time=datetime.now()
    print(f"Conexión cerrada: Código {close_status_code}, Mensaje: {close_msg}")
    
# Función que se ejecuta si ocurre un error
def on_error(ws, error):
    global credentials
    print(f"Error en WebSocket: {error}")
    connection,error1=DB_login(credentials)
    errors=["error en conexion",error1]
    errors,result=send_telegram(errors)
    upload_log(connection,os.path.basename(__file__),start_time,datetime.now(),result,errors)


while True:
    try:
        # Crear una instancia del WebSocket
        ws = websocket.WebSocketApp(
            WS_URL,
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_error=on_error,
        )

        # Iniciar la conexión (esto se ejecutará de forma bloqueante)
        print("Iniciando conexión al WebSocket...")
        ws.run_forever()
    except Exception as e:
        print(f"hay un error general {e}, volviendo a correr el bucle ")
        connection,error1=DB_login(credentials_log)
        errors=["error en conexion websocket token poliedro"]
        errors,result=send_telegram(errors)
        upload_log(connection,os.path.basename(__file__),start_time,datetime.now(),result,errors)
