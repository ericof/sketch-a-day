"""2024-12-23
Vendo o Som 4 - Heart of Glass (Blondie)
Exercício de visualização de som com espirais
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import numpy as np
import py5
import sounddevice as sd

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM_X = 200
MARGEM_Y = 200


ESPIRAIS = 8
ALL_DATA = deque([], maxlen=3000)
DEVICE = 0
GAIN = 30
BLOCK_DURATION = 10
SAMPLING_RATE = sd.query_devices(DEVICE, "input")["default_samplerate"]

CAPTURAS = 720


def callback(signal, frames, time, status):
    if any(signal):
        fft_result = np.fft.fft(signal)

        # Compute the corresponding frequencies for the FFT result
        num_samples = len(signal)
        freq_bins = np.fft.fftfreq(num_samples, d=1 / SAMPLING_RATE)

        # Compute magnitudes of the FFT (only take the positive half of the spectrum)
        magnitude = np.abs(fft_result)[: num_samples // 2]
        # magnitude *= 10 / num_samples // 2
        freq_bins = freq_bins[: num_samples // 2]

        ALL_DATA.append((freq_bins, magnitude))


def espiral(
    xb: float,
    yb: float,
    offset: float,
    data: np.array,
    frame_max: float,
    frame_min: float,
):
    pontos = []
    total_pontos = len(data)
    raio_max = py5.width * 2
    for idx in range(total_pontos):
        direcao = 1
        angulo = py5.radians(idx * 5 + offset)
        r = idx * raio_max / total_pontos
        pb = data[idx][0]
        diff = py5.remap(pb, frame_min, frame_max, 1, 1.3) * direcao
        x0 = xb + r * np.cos(angulo)
        y0 = yb + r * np.sin(angulo)
        x = x0 * diff
        y = y0 * diff
        pontos.append((x0, y0, x, y, diff))
    return pontos


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)


def draw():
    py5.background(0)
    offset_b = 360 / ESPIRAIS
    offset = 0
    with py5.push_style():
        with py5.push_matrix():
            py5.translate(py5.width // 2, py5.height // 2, -30)
            py5.rotate_x(py5.radians(py5.frame_count))
            for i in range(0, ESPIRAIS):
                py5.rotate_x(py5.radians(-5))
                data = ALL_DATA[0][1]
                frame_min = np.min(data)
                frame_max = np.max(data)
                pontos = espiral(0, 0, offset, data, frame_max, frame_min)
                for idx, (x0, y0, x, y, diff) in enumerate(pontos):
                    h = (idx * diff * 180) % 360
                    py5.stroke(py5.color(h, 90, 90))
                    weight = (idx // 100) + 2
                    py5.stroke_weight(weight)
                    py5.line(x0, y0, 0, x, y, diff * 4)
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
