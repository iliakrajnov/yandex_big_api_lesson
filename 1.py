import os
import pygame
import requests
from PIL import Image
from io import BytesIO
from toponym_envelope import get_toponym_envelope


def get_toponym():
    screen.fill((0, 0, 0))
    intro_text = ["Координаты: "]
    title = pygame.font.Font(None, 120).render("Жду.", 1, pygame.Color("white"))
    screen.blit(title, ((width - title.get_rect().width) // 2, 200))
    font = pygame.font.Font(None, 30)
    text_coord = 200 + title.get_rect().bottom
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("white"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (width - string_rendered.get_rect().width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += chr(int(event.key))
                    if len(name) > 20:
                        name = name[:20]
                title = pygame.font.Font(None, 50).render(
                    name, 1, pygame.Color("white")
                )
                pygame.draw.rect(screen, (0, 0, 0), (0, 400, 10000, 400))
                screen.blit(title, ((width - title.get_rect().width) // 2, 400))
        pygame.display.flip()


def button(q):
    pygame.draw.rect(screen, (0, 0, 255), (0, 0, 300, 50))
    data = ["map", "sat", "sat,skl", "sat,trf", "map,trf"]
    q %= len(data)
    text = pygame.font.Font(None, 24).render("Карта", 1, (255, 255, 0))
    screen.blit(text, (190, 15))
    return data[q]

def button2():
    pygame.draw.rect(screen, (0, 0, 200), (300, 0, 600, 50))
    text = pygame.font.Font(None, 24).render("сброс", 1, (255, 255, 0))
    screen.blit(text, (390, 15))



def mas_minus(spn):
    spn = spn.split(",")
    spn = ",".join([str(float(spn[0]) * 2), str(float(spn[1]) * 2)])
    return spn


def mas_plus(spn):
    spn = spn.split(",")
    spn = ",".join([str(float(spn[0]) / 2), str(float(spn[1]) / 2)])
    return spn


def get_image(ll, spn, mapp, finded_place):
    map_params = {"ll": ll, "spn": spn, "l": mapp, "pt": finded_place}
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    file = open("1.png", "wb")
    file.write(response.content)
    file.close()
    screen.blit(pygame.image.load("1.png"), (0, 50))
    pygame.display.flip()


def up(ll):
    ll = ll.split(",")
    ll = ",".join([str(float(ll[0])), str(float(ll[1]) * 1.00001)])
    return ll


def down(ll):
    ll = ll.split(",")
    ll = ",".join([str(float(ll[0])), str(float(ll[1]) / 1.00001)])
    return ll


def left(ll):
    ll = ll.split(",")
    ll = ",".join([str(float(ll[0]) / 1.00001), str(float(ll[1]))])
    return ll


def right(ll):
    ll = ll.split(",")
    ll = ",".join([str(float(ll[0]) * 1.00001), str(float(ll[1]))])
    return ll


size = width, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.init()
toponym_to_find = get_toponym()

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

ll, spn = get_toponym_envelope(toponym)
finded_place = ll + "," + "pmgnm"
q = 0
mapp = button(q)
button2()
get_image(ll, spn, mapp, finded_place)
address_to_out = toponym['metaDataProperty']['GeocoderMetaData']['text'])
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < 50 and x < 300:
                q += 1
                mapp = button(q)
                get_image(ll, spn, mapp, finded_place)
            if y < 50 and x > 300:
                toponym_to_find = get_toponym()
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

                ll, spn = get_toponym_envelope(toponym)
                finded_place = ll + "," + "pmgnm"
                q = 0
                mapp = button(q)
                button2()
                get_image(ll, spn, mapp, finded_place)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn = mas_minus(spn)
                get_image(ll, spn, mapp, finded_place)
            if event.key == pygame.K_PAGEDOWN:
                spn = mas_plus(spn)
                get_image(ll, spn, mapp, finded_place)
            if event.key == pygame.K_UP:
                ll = up(ll)
                get_image(ll, spn, mapp, finded_place)
            if event.key == pygame.K_DOWN:
                ll = down(ll)
                get_image(ll, spn, mapp, finded_place)
            if event.key == pygame.K_RIGHT:
                ll = right(ll)
                get_image(ll, spn, mapp, finded_place)
            if event.key == pygame.K_LEFT:
                ll = left(ll)
                get_image(ll, spn, mapp)
    pygame.display.flip()
pygame.quit()
