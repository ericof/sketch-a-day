"""2023-04-13"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from random import choice

import py5



IMG_NAME = Path(__file__).name.replace(".py", "")

PRIMES = []

PALETTE = [
    py5.color(0, 255, 0),
    py5.color(0, 255, 200),
    py5.color(100, 255, 80),
    py5.color(140, 235, 73),
    py5.color(50, 255, 99),
    py5.color(75, 255, 200),
]

def settings():
    py5.size(WIDTH, HEIGHT)

def setup():
    background()
    write_legend(PALETTE, IMG_NAME)
    write_text()
    draw_spiral()
    save_image(IMG_NAME)

def write_text():
    py5.fill(PALETTE[-1])
    py5.text_size(30)
    py5.text_align(py5.LEFT)
    py5.text("Espiral de Ulam", 10, 30)

def draw_spiral():
    py5.rect_mode(py5.CENTER)
    py5.translate(400, 400)
    lado = 20
    x = 0
    y = 0
    with py5.push_matrix():
        i = 1
        for elements in range (1, 30):
            for j in range(1, 3):
                for _ in range(elements):
                    if j % 2:
                        x = x - lado if elements % 2 else x + lado
                    else:
                        y = y + lado if elements % 2 else y - lado
                    i += 1
                    draw_point(x, y, lado, i)
            py5.rotate(py5.radians(-90))


def par_bagunca(faixa_bagunca):
    bx = py5.random(-faixa_bagunca, faixa_bagunca)
    by = py5.random(-faixa_bagunca, faixa_bagunca)
    return bx, by


def quadrado_molnar(x, y, lado, faixa_bagunca, preencher):
    bx, by = par_bagunca(faixa_bagunca)
    x0, y0 = x - lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x1, y1 = x + lado / 2 + bx, y - lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x2, y2 = x + lado / 2 + bx, y + lado / 2 + by
    bx, by = par_bagunca(faixa_bagunca)
    x3, y3 = x - lado / 2 + bx, y + lado / 2 + by
    if preencher:
        py5.no_stroke()
        py5.fill(preencher)
    else:
        py5.no_fill()
        py5.stroke(py5.color(0,0,0))
    py5.quad(x0, y0, x1, y1, x2, y2, x3, y3)


def draw_point(x, y, lado, i):
    lado_interno = lado - 4
    if is_prime(i):
        preenchimento = choice(PALETTE)
        # Primeiro elemento é preenchido
        bagunca = lado_interno * 0.2
        quadrado_molnar(x, y, lado_interno, bagunca, preenchimento)
        # Segundo elemento é apenas a linha
        bagunca = lado_interno * 0.05
        quadrado_molnar(x, y, lado_interno, bagunca, None)


def background():
    for i in range(0, 801):
        if i % 2:
            py5.stroke(i / 4, 0, i)
        else:
            py5.stroke(i, 0, i / 4)
        py5.line(0, i, 800, i)


def is_prime(number) -> bool:
    if number == 1:
        return False
    if not PRIMES:
        PRIMES.append(number)
        return True
    else:
        is_prime = all([True if number % i else False for i in PRIMES if i > 1])
        if is_prime:
            PRIMES.append(number)
        return is_prime

py5.run_sketch()
