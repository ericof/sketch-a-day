"""2023-12-13"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import shuffle

import numpy as np
import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

_PARTICIPANTES = [
    "Ace",
    "Adelaide Brooke",
    "Adric",
    "Amy Pond",
    "Astrid Peth",
    "Bill Potts",
    "Captain Jack Harkness",
    "Clara Oswald",
    "Craig Owens",
    "Donna Noble",
    "Érico Andrei",
    "Grace Holloway",
    "Harry Sullivan",
    "Jackson Lake",
    "K9",
    "Kamelion",
    "Lady Christina de Souza",
    "Leela",
    "Martha Jones",
    "Mel Bush",
    "Mickey Smith",
    "Nardole",
    "Nyssa",
    "Peri Brown",
    "River Song",
    "Romana I",
    "Romana II",
    "Rory Williams",
    "Rose Tyler",
    "Rosita Farisi",
    "Sarah Jane Smith",
    "Tegan Jovanka",
    "Vislor Turlough",
    "Wilfred Mott",
]
SORTEIO = []

FONT_SIZE = 121
MAIOR_NOME = ""

PLACA = (600, 250)

PLACAS = []

RAIO = 300

RODANDO = False
PROXIMO = 0


def setup():
    global FONT_SIZE
    global SORTEIO
    global PLACAS
    global RAIO
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)
    py5.text_align(py5.CENTER, py5.CENTER)
    SORTEIO = [(idx, n) for idx, n in enumerate(prepara_sorteio())]
    total = len(SORTEIO)
    shuffle(SORTEIO)
    w, h = PLACA
    FONT_SIZE = calcula_font_size(w)
    RAIO = h * total / py5.TAU
    for i in range(0, 2):
        PLACAS.append(criar_placa(i, w, h))


def calcula_font_size(w):
    font_size = 121
    fits = False
    while not fits:
        font_size -= 1
        py5.text_size(font_size)
        largura = py5.text_width(MAIOR_NOME)
        fits = largura < w * 0.80
    return font_size


def prepara_sorteio():
    global MAIOR_NOME
    for nome in _PARTICIPANTES:
        nome = nome.replace("  ", " ")
        if len(nome) > len(MAIOR_NOME):
            MAIOR_NOME = nome
    return _PARTICIPANTES


def draw():
    global RODANDO
    global PROXIMO
    global SORTEIO
    frame_count = py5.frame_count
    py5.background(py5.color(0))
    py5.translate(WIDTH // 2, HEIGHT // 2, -RAIO * 1.1)
    if RODANDO:
        ro = frame_count
    else:
        ro = PROXIMO
    w, h = PLACA
    total = len(_PARTICIPANTES)
    angulo = py5.TAU / total
    for i, nome in enumerate(_PARTICIPANTES):
        with py5.push_matrix():
            py5.rotate_x(angulo * (i + ro))
            py5.translate(0, 0, RAIO)
            placa_texto(nome, FONT_SIZE, i)
    py5.translate(0, 0, RAIO + 30)
    py5.stroke_weight(5)
    py5.stroke(360, 100, 100)
    py5.no_fill()
    py5.rect(0, 0, WIDTH - 10, h * 1.2)
    py5.translate(-WIDTH / 2, -HEIGHT / 2, 0)
    write_legend([py5.color(360, 0, 100)], img_name=IMG_NAME)
    if frame_count % 2:
        py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame_count}")


def criar_placa(idx, w, h):
    cor = (360, 0, 100) if idx % 2 else (360, 5, 100)
    traco = (360, 0, 0)
    x = w / 2
    y = h / 2
    forma = py5.create_shape()
    with forma.begin_closed_shape():
        forma.vertex(-x, -y)
        forma.vertex(+x, -y)
        forma.vertex(+x, +y)
        forma.vertex(-x, +y)
    forma.set_fill(py5.color(*cor))
    forma.set_stroke_weight(2)
    forma.set_stroke(py5.color(*traco))
    return forma


def placa_texto(texto, font_size, idx):
    forma = PLACAS[idx % 2]
    py5.shape(forma, 0, 0)
    py5.translate(0, 0, 1)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.fill(py5.color(0))
    py5.text_size(font_size)
    py5.text(texto, 0, -10)


def key_pressed():
    global PROXIMO
    global RODANDO
    global SORTEIO
    key = py5.key
    name = ""
    if key == " ":
        if RODANDO:
            RODANDO = False
            PROXIMO, name = SORTEIO.pop()
        else:
            RODANDO = True
            PROXIMO = 0


py5.run_sketch()
