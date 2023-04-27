"""2023-04-27"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from random import choice
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


GRADE = []

FUNDO = py5.color(248, 241, 219)

CORES = [
    py5.color(31, 73, 180),
    py5.color(39, 39, 39),
    # py5.color(80, 127, 180),
    # py5.color(51, 51, 52),
]


class Celula:
    """
    nova = Celula(x, y, largura, [func_desenho0, func_desenho1, ...])
    .desenha()    desenha celula na sua posição
    .gira()       gira 90 graus
    .sob_mouse()  True ou False se o mouse está sobre a célula
    .espelha()    Inverte espelhamento
    .muda_desenho()   Muda função de desenho para a próxima
    .espelhada    Estado atual de espelhamento
    .rot          Rotação atual
    .func_ativa   Índice da função de desenho atual
    """

    def __init__(self, x, y, largura, funcs):
        self.x, self.y = x, y
        self.largura = largura
        self.funcs = funcs
        self.func_ativa = choice(range(0, len(funcs)))
        self.rot = choice(range(0, 360, 90))
        self.espelhada = False
        self.cor = choice(CORES)

    def desenha(self):
        with py5.push_matrix():
            py5.translate(self.x, self.y)
            if self.espelhada:
                py5.scale(-1, 1)
            py5.rotate(py5.radians(self.rot))
            funcao_desenho = self.funcs[self.func_ativa]
            funcao_desenho(0, 0, self.largura, self.cor)

    def sob_mouse(self, x, y):
        return (
            self.x - self.largura / 2 < x < self.x + self.largura / 2
            and self.y - self.largura / 2 < y < self.y + self.largura / 2
        )

    def gira(self, rot=90):
        self.rot = self.rot + rot if self.rot < 360 else rot

    def muda_cor(self):
        self.cor = choice(CORES)

    def muda_desenho(self, i=None):
        self.func_ativa = (self.func_ativa + 1) % len(self.funcs) if i is None else i

    def espelha(self):
        self.espelhada = not self.espelhada


def modulo_01(x, y, largura, cor):
    x0 = x - largura / 2
    y0 = y - largura / 2
    py5.fill(cor)
    py5.stroke(cor)
    py5.arc(x0, y0, 2 * largura, 2 * largura, py5.radians(0), py5.radians(90))


def modulo_02(x, y, largura, cor):
    x0 = x - largura / 2
    y0 = y - largura / 2
    py5.no_fill()
    py5.stroke_weight(2)
    py5.stroke(cor)
    passos = 20
    passo = largura * 2 / passos
    for i in range(0, passos):
        largura_ = passo * i + passo
        py5.arc(x0, y0, largura_, largura_, py5.radians(0), py5.radians(90))


def popula_grade():
    linhas = 6
    colunas = 6
    margem = 100
    largura = (py5.width - (2 * margem)) / colunas
    for i in range(colunas):
        x = margem + largura / 2 + i * largura
        for j in range(linhas):
            y = margem + largura / 2 + j * largura
            celula = Celula(x, y, largura, [modulo_01, modulo_02])
            print(x, y)
            GRADE.append(celula)


def desenha_grade():
    for celula in GRADE:
        celula.desenha()


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    popula_grade()
    # save_image(IMG_NAME, "png")


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
