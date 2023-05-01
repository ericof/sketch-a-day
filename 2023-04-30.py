"""2023-04-30"""
from helpers import Celula
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


GRADE = []

FUNDO = py5.color(248, 241, 219)

CORES = [
    py5.color(10, 0, 78),
    py5.color(10, 0, 78),
    py5.color(10, 0, 78),
    py5.color(10, 0, 78),
    py5.color(10, 0, 78),
    py5.color(37, 67, 32),
]


def modulo_01(x, y, largura, cor):
    tamanho = largura // 3
    # Pontos iniciais
    x0 = x - largura / 2 + 2
    y0 = y - largura / 2 + 2
    # Pontos finais
    x1 = x + largura / 2 - 2
    y1 = y + largura / 2 - 2
    # Meio
    x2 = x1 - (tamanho // 2)
    y2 = y1 - (tamanho // 2)
    py5.fill(cor)
    py5.stroke(cor)
    with py5.begin_closed_shape():
        py5.vertex(x0, y0 + tamanho)
        py5.vertex(x0 + tamanho, y0 + tamanho)
        py5.vertex(x1 - tamanho, y0)
        py5.vertex(x1, y0 + tamanho)
        py5.vertex(x1, y1 - tamanho)
        py5.vertex(x2, y1 - tamanho)
        py5.vertex(x2, y2)
        py5.vertex(x1 - tamanho, y2)
        py5.vertex(x1 - tamanho, y1)
        py5.vertex(x0 + tamanho, y1)
        py5.vertex(x0 + tamanho, y1 - tamanho)
        py5.vertex(x0, y1 - tamanho)


def popula_grade():
    linhas = 10
    colunas = 10
    margem = 50
    largura = (py5.width - (2 * margem)) / colunas
    for i in range(colunas):
        x = int(margem + largura / 2 + i * largura)
        for j in range(linhas):
            y = int(margem + largura / 2 + j * largura)
            celula = Celula(x, y, largura, [modulo_01], CORES)
            print(x, y)
            GRADE.append(celula)


def desenha_grade():
    for celula in GRADE:
        celula.desenha()


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    popula_grade()


def draw():
    py5.background(FUNDO)
    write_legend(["#000000"], IMG_NAME)
    desenha_grade()


def mouse_pressed():
    for celula in GRADE:
        if celula.sob_mouse(py5.mouse_x, py5.mouse_y):
            if (
                py5.mouse_button == py5.LEFT
                and py5.is_key_pressed
                and py5.key_code == py5.SHIFT
            ):
                celula.muda_cor()
                print("Altera cor")
            elif py5.mouse_button == py5.LEFT:
                rot = celula.rot
                celula.gira()
                print(f"Gira de {rot} até {celula.rot}")
            elif py5.mouse_button == py5.RIGHT:
                celula.muda_desenho()
                print("Muda desenho")


def key_pressed():
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
