import requests
from Test.olla_config import OLLATOKEN

def get_images():
    # Configura la conexión a OLLA
    olla_token = OLLATOKEN
    olla_url = "http://localhost:8501/"


    # Envía una solicitud a la API de OLLA para obtener las imágenes
    headers = {"Authorization": f"Bearer {olla_token}"}
    response = requests.get(olla_url + "images", headers=headers)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsea el JSON y extrae las URLs de las imágenes
        images_json = response.json() #response.text(), response
        image_urls = [image["url"] for image in images_json]

        # Carga cada imagen y muestra sus detalles
        for url in image_urls:
            img_response = requests.get(url)
            img = Image.open(BytesIO(img_response.content))
            print(f"Imagen: {url}")
            print(f"Tamaño: {img.size}")
            print(f"Formato: {img.format}\n")
    else:
        print("Error al obtener las imágenes")

if __name__ == "__main__":
    get_images()