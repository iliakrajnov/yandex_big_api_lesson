import os
import pygame
import requests
from PIL import Image
from io import BytesIO
import geocoder


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


def button3(color, c):
    pygame.draw.rect(screen, color, (600, 0, 650, 500))
    if c == 't':
        text = pygame.font.Font(None, 24).render("выкл.", 1, (0, 0, 0))
    else:
        text = pygame.font.Font(None, 24).render("вкл.", 1, (0, 0, 0))
    screen.blit(text, (605, 250))


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


size = width, height = 650, 500
screen = pygame.display.set_mode(size)
pygame.init()
toponym_to_find = get_toponym()
ll, spn = geocoder.get_ll_span(toponym_to_find)
finded_place = ll + "," + "pmgnm"
q = 0
mapp = button(q)
button2()
button3((255, 0, 0), 't')
u = 0
get_image(ll, spn, mapp, finded_place)
while 1:
    address_to_out = geocoder.geocode(toponym_to_find)['metaDataProperty']['GeocoderMetaData']['text']
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
            elif y < 50 and x > 300 and x < 600:
                toponym_to_find = get_toponym()
                ll, spn = geocoder.get_ll_span(toponym_to_find)
                finded_place = ll + "," + "pmgnm"
                q = 0
                mapp = button(q)
                button2()
                get_image(ll, spn, mapp, finded_place)

            elif x > 600:
                u += 1
                if u % 2 == 0:
                    button3((255, 0, 0), 't')
                else:
                    button3((0, 255, 0), 'f')
            else:
                pix_x = float(spn.split(',')[0]) / 600
                pix_y = float(spn.split(',')[1]) / 450
                print(pix_x, pi)
                zero = (300, 275)
                print(ll)
                print(float(ll.split(',')[0]) + (zero[0] - x) * pix_x, float(ll.split(',')[1]) + (zero[1] - y) * pix_y)
                #print(geocoder.get_nearest_object((f_x + pix_x * x, f_y - pix_y * y), 'house'))
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
    coords = ', '.join(list(map(str, geocoder.get_coordinates(toponym_to_find))))
    try:
        postal = geocoder.geocode(coords)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    except KeyError:
        postal = 'Нет индекса'
    if u % 2 == 0:
        get_image(ll, spn, mapp, finded_place)
        text = pygame.font.Font(None, 24).render(address_to_out, 1, (255, 0, 0))
    else:
        get_image(ll, spn, mapp, finded_place)
        text = pygame.font.Font(None, 24).render(address_to_out + ' ' + postal, 1, (255, 0, 0))
    screen.blit(text, (0, 450))
    pygame.display.flip()
pygame.quit()
