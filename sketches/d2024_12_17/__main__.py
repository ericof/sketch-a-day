"""2024-12-17
Formas Geométricas 6 (Modern Love, David Bowie)
Exercício de grade de formas geométricas
png
Sketch,py5,CreativeCoding
"""

import math
from random import shuffle

import numpy as np
import py5
import sounddevice as sd

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 300
MARGEM_Y = 200

TAMANHO = 45
PASSO = 30

DEVICE = 0
GAIN = 20
BLOCK_DURATION = 24


def octagono() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(30, 0)
        s.vertex(60, 0)
        s.vertex(90, 30)
        s.vertex(90, 60)
        s.vertex(60, 90)
        s.vertex(30, 90)
        s.vertex(0, 60)
        s.vertex(0, 30)
    return s


def hexagono() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(30, 0)
        s.vertex(60, 0)
        s.vertex(90, 45)
        s.vertex(60, 90)
        s.vertex(30, 90)
        s.vertex(0, 45)
    return s


def quadrado() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(0, 0)
        s.vertex(90, 0)
        s.vertex(90, 90)
        s.vertex(0, 90)
        s.vertex(0, 0)
    return s


def capture_sound(total_points: int):
    data = []
    samplerate = sd.query_devices(DEVICE, "input")["default_samplerate"]
    low, high = [100, 2000]
    delta_f = (high - low) / (80 - 1)
    fftsize = math.ceil(samplerate / delta_f)

    def callback(indata, frames, time, status):
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
            magnitude *= 10 / fftsize
            rot = py5.random_int(0, 90)
            data.append((magnitude, rot))

    with sd.InputStream(
        device=DEVICE,
        channels=1,
        callback=callback,
        blocksize=int(samplerate * BLOCK_DURATION / 1000),
        samplerate=samplerate,
    ):
        while len(data) < total_points:
            print(f"{len(data)}/{total_points} ({samplerate})")
    return data


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CENTER)
    formas = [hexagono(), octagono(), quadrado()]
    pontos = []
    angulos = range(0, 180, 3)

    for idy, y in enumerate(range(-MARGEM_Y, py5.height + MARGEM_Y, PASSO)):
        buffer_x = 0 if idy % 2 else TAMANHO // 2
        for idx, x in enumerate(range(-MARGEM_X, py5.width + MARGEM_X, PASSO)):
            forma = formas[py5.random_int(0, 2)]
            angulo = py5.random_choice(angulos)
            pontos.append((x + buffer_x, y, forma, angulo))
            idx += 1
        shuffle(pontos)
    data = capture_sound(len(pontos))
    with py5.push_matrix():
        py5.translate(0, 0, -20)
        for idx, (x, y, forma, ang_rot) in enumerate(pontos):
            info = data[idx]
            ang_rot_2 = info[1]
            forma.set_stroke_weight(2)
            h = py5.remap(np.median(info[0]), 0, 0.001, 0, 360)
            s = py5.remap(np.max(info[1]), 0, 0.1, 50, 100)
            cor = py5.color(h, 0, 0)
            forma.set_stroke(cor)
            cor = py5.color(h, s, 70)
            forma.set_fill(cor)
            with py5.push_matrix():
                py5.translate(x, y)
                py5.rotate(py5.radians(ang_rot + ang_rot_2))
                py5.shape(forma, 0, 0, TAMANHO, TAMANHO)
    helpers.write_legend(sketch=sketch, frame="#000")


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
