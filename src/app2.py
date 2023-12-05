from bs4 import BeautifulSoup
import requests
import urllib.parse

def get_high_resolution_url(image_url):
    return image_url.replace('=s', '=s0')

def search_image_links(search, max_links):
    base_url = "https://www.google.com"
    url = base_url + "/search?tbm=isch&q=" + urllib.parse.quote(search)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    image_links = []

    for i, imagen in enumerate(images):
        if len(image_links) >= max_links:
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

            image_links.append(url_imagen_high_res)
        except KeyError:
            pass

    return image_links

max_links = 10
image_links = search_image_links("GTA V", max_links)

# Imprimir los enlaces
for i, link in enumerate(image_links):
    print(f"Enlace {i+1}: {link}")
