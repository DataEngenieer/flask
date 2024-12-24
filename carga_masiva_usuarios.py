# Importandopaquetes desde flask
from flask import session, flash
import pandas as pd
from conexion.conexionBD import connectionBD
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

#from conexion.conexionBD import connectionBD

from werkzeug.security import generate_password_hash
from controllers.funciones_login import *

def recibeInsertRegisterUser(documento, name_surname, email_user, pass_user, rol, token, numero_token, campaing):
    # Validar los datos del usuario
    respuestaValidar = validarDataRegisterLogin(name_surname, email_user, pass_user)

    if respuestaValidar:
        # Generar hash de la contraseña
        nueva_password = generate_password_hash(pass_user, method='scrypt')
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = "INSERT INTO users(documento, name_surname, email_user, pass_user, rol, token, numero_token, campaing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    valores = (documento, name_surname, email_user, nueva_password, rol, token, numero_token, campaing)
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert
        except Exception as e:
            print(f"Error en el Insert users: {e}")
            return []
    else:
        return False

def registrar_usuarios_excel(ruta_excel, rol_predeterminado):
    try:
        # Leer el archivo Excel
        df = pd.read_excel(ruta_excel)
        df = df.astype(str)
        
        # Iterar sobre cada fila del DataFrame
        for _, row in df.iterrows():
            name_surname = row['name_surname']
            email_user = row['email_user']
            documento = row['documento']
            pass_user = row['pass_user']
            token = row['token']
            numero_token = row['numero_token']
            campaing = row['campaing']
            # Llamar a la función para insertar el usuario
            resultado = recibeInsertRegisterUser(
                documento=documento,
                name_surname=name_surname,
                email_user=email_user,
                pass_user=pass_user,
                token=token,
                numero_token=numero_token,
                campaing=campaing,
                rol=rol_predeterminado
            )
            
            if resultado:
                print(f"Usuario {name_surname} registrado correctamente.")
            else:
                print(f"Error al registrar el usuario {name_surname}.")
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")


ruta_excel = 'usuarios1.xlsx'  # Ruta del archivo Excel
rol_predeterminado = 'agente'  # Rol predeterminado para los usuarios

registrar_usuarios_excel(ruta_excel, rol_predeterminado)