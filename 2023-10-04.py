"""2023-10-04"""
from helpers import CelulaV4 as Celula
from helpers import Grade
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(0),
]

LADO = 50
PONTOS_PAR = [
    [
        (0, LADO),
        (LADO, 0),
        (LADO, LADO),
        (0, LADO),
    ],
    [
        (0, 0),
        (LADO, 0),
        (LADO, LADO),
        (0, LADO),
        (0, 0),
    ],
    [
        (0, 0),
        (LADO, LADO),
        (0, LADO),
        (0, 0),
    ],
    [],
]
PONTOS_IMPAR = [
    [],
    [
        (0, 0),
        (LADO, LADO),
        (LADO, 0),
        (0, 0),
    ],
    [
        (0, 0),
        (LADO, 0),
        (LADO, LADO),
        (0, LADO),
        (0, 0),
    ],
    [
        (0, LADO),
        (LADO, 0),
        (0, 0),
        (0, LADO),
    ],
]


def forma_completa():
    lado = 50
    pontos = [
        (0, lado),
        (lado, 0),
        (2 * lado, 0),
        (3 * lado, lado),
        (4 * lado, lado),
        (3 * lado, 2 * lado),
        (2 * lado, 2 * lado),
        (lado, lado),
        (0, lado),
    ]
    s = py5.create_shape()
    with s.begin_shape():
        for x, y in pontos:
            s.vertex(x, y)
    return s


def _factory(pontos):
    s = py5.create_shape()
    with s.begin_shape():
        for x, y in pontos:
            s.vertex(x, y)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(200))
    formas_par = [_factory(pontos) for pontos in PONTOS_PAR]
    formas_impar = [_factory(pontos) for pontos in PONTOS_IMPAR]
    linhas = 16
    colunas = 16
    margem = 40
    largura = (py5.width - (2 * margem)) / colunas
    grade = Grade(0, 0, WIDTH, HEIGHT, colunas, linhas, margem, margem)
    for idx, slot in enumerate(grade):
        linha = idx // colunas
        # formas = formas_par if linha % 2 == 0 else formas_impar
        formas = formas_par if linha % 2 == 0 else formas_impar
        coluna = idx % colunas
        coluna_interna = coluna % 4
        forma = formas[coluna_interna]
        celula = Celula(
            slot.x,
            slot.y,
            largura,
            [
                forma,
            ],
            CORES,
            border=0,
        )
        celula.espelhada = False
        slot.celulas.append(celula)
    grade.desenha()
    write_legend([py5.color(0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
