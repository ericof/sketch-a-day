"""2024-12-24
Vendo o Som 5 - Blue Monday (New Order)
Exercício de visualização de som com espirais
png
Sketch,py5,CreativeCoding
"""

import math
from collections import deque

import numpy as np
import py5
import sounddevice as sd

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 200
MARGEM_Y = 200


CIRCULOS = 20
ALL_DATA = deque([], maxlen=3000)
DEVICE = 0
GAIN = 30
BLOCK_DURATION = 10
SAMPLING_RATE = sd.query_devices(DEVICE, "input")["default_samplerate"]

CAPTURAS = 720


def callback(signal, frames, time, status):
    low, high = [100, 2000]
    delta_f = (high - low) / (80 - 1)
    fftsize = math.ceil(SAMPLING_RATE / delta_f)
    if any(signal):
        # Compute the corresponding frequencies for the FFT result
        num_samples = len(signal)
        freq_bins = np.fft.fftfreq(num_samples, d=1 / SAMPLING_RATE)

        fft_result = np.fft.rfft(signal[:, 0], n=fftsize)
        magnitude = np.abs(fft_result)[: num_samples // 2]
        # magnitude *= 10 / num_samples // 2
        freq_bins = freq_bins[: num_samples // 2]
        ALL_DATA.append((freq_bins, magnitude))


def circulo(mult, data, frame_max, frame_min):
    pontos = []
    total = len(data)
    passo = 360 / total
    for idx in range(0, total):
        direcao = 1
        pb = data[idx]
        z = py5.remap(pb, frame_min, frame_max, 1, 40) * direcao
        angulo = idx * passo
        x0 = np.cos(py5.radians(angulo)) * mult
        y0 = np.sin(py5.radians(angulo)) * mult
        pontos.append((x0, y0, 0, x0, y0, z))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)


def draw_circle(data, peso, mult, zb, b):
    frame_min = np.min(data)
    frame_max = np.max(data)
    pontos = circulo(mult, data, frame_max, frame_min)
    py5.stroke_weight(peso)
    for x0, y0, z0, x, y, z in pontos:
        h = (((z - z0) * 1.8) % 180) + 180
        py5.stroke(py5.color(h, 90, b))
        py5.line(x0, y0, zb + z0, x, y, zb + z)


def draw():
    py5.background(0)
    passo = 1200 / (CIRCULOS * 2)
    offset_b = 360 / CIRCULOS
    offset = 0
    with py5.push_style():
        with py5.push_matrix():
            py5.translate(py5.width // 2, py5.height // 2, -30)
            py5.rotate_x(py5.radians(45))
            for i in range(0, CIRCULOS):
                b = ((CIRCULOS - i) / CIRCULOS) * 90 + 10
                for divisor in range(1, 2):
                    zb = i * 10
                    peso = np.abs((CIRCULOS - i + 1) / 3)
                    data = ALL_DATA[0][1]
                    mult = (i + 1) * (passo / divisor)
                    draw_circle(data, peso, mult, zb, b)
                    py5.rotate_z(py5.radians(-5))
                    offset += offset_b
                    ALL_DATA.rotate()

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
    with sd.InputStream(
        device=DEVICE,
        channels=1,
        callback=callback,
        blocksize=int(SAMPLING_RATE * BLOCK_DURATION / 1000),
        samplerate=SAMPLING_RATE,
    ):
        py5.run_sketch()
