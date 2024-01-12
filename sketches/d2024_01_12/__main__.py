"""2024-01-12
Genuary 12 - Lava lamp
Animação representando a simulação de uma lava lamp.
gif
Sketch,py5,CreativeCoding,genuary,genuary12
"""
import numpy as np
import py5
import py5_tools

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

FRAMES = 500

CORES = np.uint8([[0, 255, 165, 0], [0, 255, 100, 50]])
YMAX = 0.82
XMAX = 1.25
Y, X = np.ogrid[YMAX : -YMAX : helpers.ALTURA * 1j, -XMAX : XMAX : helpers.LARGURA * 1j]
CY = np.sin(2 * (Y + X)) * np.cos(X)
CX = np.sin(3 * X) + np.cos(X)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)


def draw():
    frame = (py5.frame_count) % FRAMES
    phase = py5.TAU * (frame / FRAMES)
    plane = CX * np.cos(Y + phase) > CY * np.sin(Y + phase)
    pontos = CORES[plane.astype(np.uint8)]
    py5.load_np_pixels()
    py5.np_pixels[::] = pontos[::-1]
    py5.update_np_pixels()
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    py5.exit_sketch()


if __name__ == "__main__":
    py5_tools.animated_gif(
        f"{sketch.path}/{sketch.day}.gif",
        count=50,
        period=0.05,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
