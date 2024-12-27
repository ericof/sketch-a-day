"""2024-12-27
Vendo o Som 8 - Syncronicity II (The Police)
Exercício de visualização de som com círculos
png
Sketch,py5,CreativeCoding
"""

import math

import numpy as np
import py5
import sounddevice as sd

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


CIRCULOS = 12
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
        # Compute the corresponding frequencies for the FFT result
        num_samples = len(signal)
        freq_bins = np.fft.fftfreq(num_samples, d=1 / SAMPLING_RATE)

        fft_result = np.fft.rfft(signal[:, 0], n=fftsize)
        magnitude = np.abs(fft_result)
        magnitude *= GAIN / fftsize
        freq_bins = freq_bins
        ALL_DATA.append((freq_bins, magnitude))


def circulo(mult, data, frame_max, frame_min, offset):
    pontos = []
    total = len(data)
    passo = 360 / total
    for idx in range(0, total):
        direcao = 1
        pb = data[idx]
        z = py5.remap(pb, frame_min, frame_max, 0, 80) * direcao
        angulo = idx * passo + offset
        x0 = np.cos(py5.radians(angulo)) * mult
        y0 = np.sin(py5.radians(angulo)) * mult
        z0 = np.sin(py5.radians(angulo)) * mult
        pontos.append((x0, y0, z0, x0, y0, z0 + z))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    while len(ALL_DATA) < 100:
        print(len(ALL_DATA))


def draw_circle(data, peso, mult, zb, hb, b, offset):
    frame_min = np.min(data)
    frame_max = np.max(data)
    pontos = circulo(mult, data, frame_max, frame_min, offset)
    py5.stroke_weight(peso)
    for x0, y0, z0, x, y, z in pontos:
        h = (((z - z0) * 1.8) % 180) * 2 + hb
        py5.stroke(py5.color(h, 90, b))
        py5.line(x0, y0, zb + z0, x, y, zb + z)


def draw():
    py5.background(60, 5, 5)
    passo = 900 / (CIRCULOS * 3)
    offset_b = 720 / CIRCULOS * 2
    offset = 180
    # Copy data to local list
    idx0 = py5.frame_count
    idx1 = py5.frame_count + CIRCULOS * 4
    local_data = [item for item in ALL_DATA[idx0:idx1:2]]
    print(idx0, idx1, len(ALL_DATA))
    with py5.push_style():
        with py5.push_matrix():
            py5.translate(py5.width // 2, py5.height // 2, -20)
            py5.rotate_y(py5.radians(20))
            for i in range(0, CIRCULOS):
                hb = ((CIRCULOS - i) / CIRCULOS) * 60
                b = ((CIRCULOS - i) / CIRCULOS) * 80 + 20
                py5.rotate_x(py5.radians(i / 2))
                for divisor in range(1, 2):
                    zb = py5.cos(py5.radians(i * (360 / CIRCULOS))) * 10
                    peso = np.abs((CIRCULOS - i + 1) / 5)
                    data = local_data.pop()[1]
                    mult = (i + 1) * (passo / divisor)
                    draw_circle(data, peso, mult, zb, hb, b, offset)
                    offset += offset_b

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
