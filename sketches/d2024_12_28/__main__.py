"""2024-12-28
Vendo o Som 9 - Success (Sigue Sigue Sputnik)
Exercício de visualização de som
png
Sketch,py5,CreativeCoding,Sound
"""

import math

import numpy as np
import py5
import sounddevice as sd

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


ALL_DATA = []
DEVICE = 0
GAIN = 50
BLOCK_DURATION = 10
SAMPLING_RATE = sd.query_devices(DEVICE, "input")["default_samplerate"]


def callback(signal, frames, time, status):
    low, high = [100, 2000]
    delta_f = (high - low) / (80 - 1)
    fftsize = math.ceil(SAMPLING_RATE / delta_f)
    if any(signal):
        fft_result = np.fft.rfft(signal[:, 0], n=fftsize)
        magnitude = np.abs(fft_result)
        magnitude *= GAIN / fftsize
        ALL_DATA.append(magnitude)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    while len(ALL_DATA) < 400:
        print(len(ALL_DATA))


def draw():
    py5.background(60, 5, 5)
    pontos = []
    local_data = ALL_DATA[-200:]
    for yb, line in enumerate(local_data):
        values = list(line)
        total = len(values)
        v_max = max(values)
        v_min = min(values)
        y = yb * 8 - (py5.height)
        for idx, value in enumerate(values):
            x = (idx - total / 2) * 3 + 400
            z = py5.remap(value, v_min, v_max, -25, 25)
            h = 40 + (abs(z) * 8)
            s = py5.remap(z, -25, 25, 70, 100)
            b = py5.remap(z, -25, 25, 70, 100)
            cor = py5.color(h, s, b)
            pontos.append((x, y, 0, x, y, z, cor))
    with py5.push_style():
        with py5.push_matrix():
            py5.translate(py5.width // 2, py5.height // 2, -40)
            py5.rotate_x(py5.radians(45))
            py5.rotate_z(py5.radians(90))
            xa, ya, za = None, None, None
            for x0, y0, z0, x1, y1, z1, cor in pontos:
                py5.stroke(cor)
                if not xa:
                    py5.point(x1, y1, z1)
                else:
                    py5.line(xa, ya, za, x1, y1, z1)
                xa, ya, za = x1, y1, z1
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
