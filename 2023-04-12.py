"""2023-04-12"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5



IMG_NAME = Path(__file__).name.replace(".py", "")

PRIMES = []

PALETTE = ["#FFFFFF"]

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
    lado = 2
    x = 0
    y = 0
    with py5.push_matrix():
        py5.stroke("#000000")
        py5.square(x, y, lado - 2)
        py5.stroke("#FF0000")
        i = 1
        for elements in range (1, 322):
            for j in range(1, 3):
                for _ in range(elements):
                    if j % 2:
                        x = x - lado if elements % 2 else x + lado
                    else:
                        y = y + lado if elements % 2 else y - lado
                    i += 1
                    draw_point(x, y, lado, i)
            py5.rotate(py5.radians(-90))


def draw_point(x, y, lado, i):
    if is_prime(i):
        py5.stroke("#FF0000")
        py5.circle(x, y, lado - 1)
    else:
        py5.stroke("#222222")
        py5.square(x, y, lado - 1)


def background():
    py5.background("#000000")


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
