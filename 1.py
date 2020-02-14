import os
import pygame
import requests
from PIL import Image
from io import BytesIO
from toponym_envelope import get_toponym_envelope


def mas_minus(spn):
    spn = spn.split(",")
    spn = ",".join([str(float(spn[0]) * 2), str(float(spn[1]) * 2)])
    return spn


def mas_plus(spn):
    spn = spn.split(",")
    spn = ",".join([str(float(spn[0]) / 2), str(float(spn[1]) / 2)])
    return spn


def get_image(ll, spn):
    map_params = {"ll": ll, "spn": spn, "l": "map"}
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    file = open("1.png", "wb")
    file.write(response.content)
    file.close()
    screen.blit(pygame.image.load("1.png"), (0, 50))
    pygame.display.flip()


size = width, height = 600, 500
screen = pygame.display.set_mode(size)

toponym_to_find = "Москва, ул. Академика Королева 12"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json",
}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"
]

pygame.init()
ll, spn = get_toponym_envelope(toponym)
get_image(ll, spn)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn = mas_minus(spn)
                get_image(ll, spn)
            if event.key == pygame.K_PAGEDOWN:
                spn = mas_plus(spn)
                get_image(ll, spn)
    pygame.display.flip()
pygame.quit()
