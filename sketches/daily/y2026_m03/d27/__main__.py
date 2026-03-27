"""2026-03-27
Ruídos 02
Padrão de ruídos gerados a partir de Perlin Noise, com variações de cor e tamanho.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

passo = 12
multiplicador = 0.025


def setup():
    global seed
    py5.size(*helpers.DIMENSOES.external, py5.P2D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)
    seed = int(py5.random(5000))


def padrao(
    n_seed: int, idx: int, max_largura: float, max_altura: float, margem: float = 0
):
    py5.noise_seed(n_seed)
    py5.no_stroke()
    py5.fill(0)
    py5.rect(margem, margem, max_largura - margem * 2, max_altura - margem * 2)
    f = idx
    xb = margem
    cor_base = 60
    while xb < max_largura - margem:
        yb = margem
        idy = 0
        while yb < max_altura - margem:
            buffer = 0.0
            if idy % 2:
                h_base = abs(cor_base - 180)
                buffer = passo * 0.5
            else:
                h_base = cor_base
            h = max(
                passo
                * py5.noise(
                    xb * multiplicador, (yb + f) * multiplicador, f * multiplicador
                ),
                passo * 0.1,
            )
            b = py5.remap(h, 0, 10, 30, 100)
            h_final = int(h_base + h * 3) % 360
            cor = py5.color(h_final, 100, b)
            py5.fill(cor)
            largura = min(passo, h)
            altura = (passo + h) / 3
            x = xb + buffer
            y = yb + buffer
            py5.ellipse(x, y, largura, altura)
            yb += h
            idy += 1
        xb += passo


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        padrao(seed, py5.frame_count, *helpers.DIMENSOES.internal, margem=0)

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
