"""2025-01-20
Generative Architecture
Casas, casas e mais casas
png
Sketch,py5,CreativeCoding,genuary,genuary2025,genuary20
"""

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

LARGURA = 80
ALTURA = 80

PALETA = [
    [
        (150, 100, 50),
        (200, 50, 50),
        (100, 50, 0),
        (200, 200, 255),
    ],
    [
        (150, 80, 75),
        (200, 50, 50),
        (100, 50, 0),
        (200, 200, 255),
    ],
    [
        (150, 90, 120),
        (200, 50, 50),
        (100, 50, 0),
        (200, 200, 255),
    ],
]

PROFUNDIDADE = 5

ELEMENTOS = [
    {
        "pos": (0, 0, 0),
        "cor": 0,
        "func": py5.box,
        "dimensoes": (160, 140, 180),
    },
    {
        "pos": (0, 25, 101),
        "cor": 2,
        "func": py5.box,
        "dimensoes": (40, 80, PROFUNDIDADE),
    },
    {
        "pos": (-60, -20, 101),
        "cor": 3,
        "func": py5.box,
        "dimensoes": (40, 40, PROFUNDIDADE),
    },
    {
        "pos": (-80, 0, 0),
        "cor": 3,
        "func": py5.box,
        "dimensoes": (PROFUNDIDADE, 80, 100),
    },
    {
        "pos": (0, -70, 0),
        "forma": py5.TRIANGLES,
        "cor": 1,
        "lados": [
            [(-110, 0, 110), (110, 0, 110), (0, -60, 0)],
            [(-110, 0, -110), (110, 0, -110), (0, -60, 0)],
            [(-110, 0, 110), (-110, 0, -110), (0, -60, 0)],
            [(110, 0, 110), (110, 0, -110), (0, -60, 0)],
        ],
    },
]


def desenha_casa():
    for elemento in ELEMENTOS:
        paleta = py5.random_choice(PALETA)
        with py5.push_matrix():
            py5.translate(*elemento["pos"])
            cor = paleta[elemento["cor"]]
            py5.fill(*cor)
            if func := elemento.get("func"):
                func(*elemento["dimensoes"])
            elif forma := elemento.get("forma"):
                lados = elemento.get("lados")
                with py5.begin_shape(forma):
                    for lado in lados:
                        for vertice in lado:
                            py5.vertex(*vertice)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.lights()
    passo_x = 400
    for idy, y in enumerate(range(-2000, 2400, 400)):
        for xb in range(-2000, 2400, passo_x):
            x = xb if idy % 2 else xb + passo_x // 2
            with py5.push_matrix():
                py5.translate(x, y, -2500)
                py5.rotate_x(py5.radians(-25))
                py5.rotate_y(py5.QUARTER_PI)
                desenha_casa()
    helpers.write_legend(sketch=sketch, cor="#FFF", frame="#000")


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
