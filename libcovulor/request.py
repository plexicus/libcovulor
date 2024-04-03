import requests

def Request():
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Ejemplo de URL de una API de prueba
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error al hacer la consulta: {response.status_code}"