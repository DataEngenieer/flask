import requests

# Configura tu token de acceso
access_token = "o.eVefl27l3Oxif6P2FaUn3y7k2T4AwI8E"

# URL de la API
url = "https://api.pushbullet.com/v2/users/me"

# Encabezados de la solicitud
headers = {
    "Access-Token": access_token
}

# Realizar la solicitud GET
response = requests.get(url, headers=headers)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    print("Respuesta exitosa:")
    print(response.json())  # Mostrar el resultado como JSON
else:
    print(f"Error {response.status_code}: {response.text}")
