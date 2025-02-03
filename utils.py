import hashlib
import random
import string


def generar_codigo_unico():
    """Genera un código corto aleatorio para la URL."""
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choices(caracteres, k=6))  # Genera una cadena de 6 caracteres
    return codigo

def acortar_url(url_larga):
    """Acorta una URL generando un código único."""
    codigo = generar_codigo_unico()
    url_corta = f"https://herramientas-qmas.up.railway.app/{codigo}"  # La URL corta será esta
    return codigo, url_corta

