"""2023-05-15"""
from helpers import HEIGHT
from helpers import save_frame
from helpers import write_legend
from helpers import save_gif
from helpers import tmp_path
from helpers import WIDTH
from pathlib import Path


import py5


IMG_NAME = Path(__file__).name.replace(".py", "")
PATH = tmp_path()

FRAMES = []

SEQUENCIA = [2, 3, 5, 8, 13, 21]
DIAMETROS = []
CENTRO_X = WIDTH / 2
CENTRO_Y = HEIGHT / 2

passo = 0
lines = 0


def settings():
    py5.size(WIDTH, HEIGHT, py5.P2D)


def setup():
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    fator = CENTRO_X // SEQUENCIA[-1]
    for item in SEQUENCIA[:-1]:
        DIAMETROS.append(item * fator)
    py5.frame_rate(5)


def draw():
    global passo, lines

    frame = py5.frame_count
    total_diametros = len(DIAMETROS)
    limite = total_diametros * 5
    idx = frame // 5 if frame < limite else 0
    b_idx = idx if frame < limite else limite
    b = ((100 - 10) // total_diametros) * b_idx + 10
    py5.stroke(py5.color(360, 0, b))
    py5.stroke_weight(2)
    py5.no_fill()
    py5.rect_mode(py5.CENTER)
    py5.ellipse_mode(py5.CORNERS)

    with py5.push_matrix():
        py5.translate(CENTRO_X, CENTRO_Y)
        diametro = DIAMETROS[idx]
        raio = diametro / 2
        if passo == 4:
            diametro = DIAMETROS[idx - 1] if idx else DIAMETROS[4]
            py5.square(0, 0, diametro * 2)
        elif passo < 4:
            for _ in range(0, passo + 1):
                py5.rotate(py5.radians(90))
            py5.ellipse(0, -raio, diametro, raio)
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")
    write_legend([py5.color(360, 0, 100)], img_name=IMG_NAME)
    FRAMES.append(save_frame(PATH, IMG_NAME, frame))
    if frame < limite:
        passo = passo + 1 if passo < 4 else 0
    else:
        with py5.push_matrix():
            py5.translate(CENTRO_X, CENTRO_Y)
            if lines == 1:
                py5.line(-diametro, -diametro, diametro, diametro)
            elif lines == 2:
                py5.line(-diametro, diametro, diametro, -diametro)
            elif lines == 3:
                py5.line(-diametro, 0, diametro, 0)
            elif lines == 4:
                py5.line(0, diametro, 0, -diametro)
            elif lines > 4:
                # Finito
                py5.no_loop()
        lines += 1


def key_pressed():
    global tamanho_pixel
    key = py5.key
    if key == " ":
        py5.no_loop()
        save_gif(IMG_NAME, FRAMES)
        py5.exit_sketch()
    elif py5.key_code == 38:
        print(tamanho_pixel)
        tamanho_pixel += 1
    elif py5.key_code == 40:
        print(tamanho_pixel)
        tamanho_pixel -= 1


py5.run_sketch()
