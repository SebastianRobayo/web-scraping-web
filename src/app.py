from bs4 import BeautifulSoup
import requests
import os
import urllib.parse

def download_image(url, filename):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, stream=True)
        with open(filename, 'wb') as file:
            file.write(response.content)
        return True
    except Exception as e:
        print(f"Error al descargar la imagen {url}: {e}")
        return False

def get_high_resolution_url(image_url):
    return image_url.replace('=s', '=s0')

def search_images(search, max_images):
    base_url = "https://www.google.com"
    url = base_url + "/search?tbm=isch&q=" + urllib.parse.quote(search)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    if not os.path.exists('images'):
        os.makedirs('images')

    image_count = 0
    downloaded_images = set()

    for i, imagen in enumerate(images):
        if image_count >= max_images:
            break
        try:
            url_imagen = imagen['src']
            if url_imagen.startswith('data:'):
                continue
            if url_imagen.startswith('/'):
                url_imagen = base_url + url_imagen

            response = requests.head(url_imagen, allow_redirects=True)
            url_imagen = response.url

            url_imagen_high_res = get_high_resolution_url(url_imagen)

            if url_imagen_high_res not in downloaded_images:
                filename = f'images/image{i}.jpg'
                if download_image(url_imagen_high_res, filename):
                    downloaded_images.add(url_imagen_high_res)
                    image_count += 1
        except KeyError:
            pass

search_images("poco x3 pro", 10)
