"""2023-04-08"""
from py5 import *
from pathlib import Path


FOLDER = Path(__file__).parent.resolve()
IMG_FOLDER = FOLDER / 'images'

# Reference https://decimal.info/digits-of-pi/value-of-pi-to-359-decimal-places.html
PI = "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036"  # noQA

# Reference https://www.heavy.ai/blog/12-color-palettes-for-telling-better-stories-with-your-data
PALETTE = [
    "#0000b3",
    "#0010d9",
    "#0020ff",
    "#0040ff",
    "#0060ff",
    "#0080ff",
    "#009fff",
    "#00bfff",
    "#00ffff",
    "#0fffff",
]


def settings():
    size(800, 800)

def setup():
    fundo()
    write_border()
    pi_circle()
    write_text()
    img = get(0, 0, 800, 800)
    img.save(IMG_FOLDER / "2023-04-08.jpg")

def fundo():
    background("#8cb596")


def write_text():
    fill("#0000b3")
    text_size(200)
    text_align(CENTER)
    text("π", 400, 430)

def write_border():
    chars = [char for char in PI]
    chars.insert(1, ".")
    chars = "".join(chars)
    fill("#0000ff")
    text_size(17)
    text_align(CENTER)
    push_matrix()
    translate(400, 400)
    for i in range(0, 4):
        text(chars[i * 90: i * 90 + 90], 0, -380)
        rotate(radians(90))
    pop_matrix()


def pi_circle():
    push_matrix()
    translate(400, 400)
    radius = -300
    for i in range(0, 360):
        # Always rotate 1 degree
        rotate(radians(1))
        digit = int(PI[i])
        start = radius
        for j in range(0, digit + 1):
            size = 12
            end = start + size if i else start - size
            stroke(PALETTE[j])
            line(0, start, 0, end)
            start = end
    pop_matrix()


run_sketch()
