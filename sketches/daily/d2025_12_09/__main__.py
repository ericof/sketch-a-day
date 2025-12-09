"""2025-12-09
Particles 02
Sistema de partículas dinâmico com divisão e movimento giratório.
ericof.com|https://abav.lugaralgum.com/sketch-a-day/#sketch_2025_12_03
png
Sketch,py5,CreativeCoding
"""

from itertools import product
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

particles = []

BORDA: int = 0
PASSO: int = 200
ALEATORIO: int = PASSO // 2
DIAMETRO: float = 60.0
REPETICOES: int = 6
Z_BASE: int = -50


class Particle:
    def __init__(self, x, y, z, d=None, v=None, h=None):
        self.pos = py5.Py5Vector(x, y)
        self.z = z
        self.vel = v or py5.Py5Vector2D.random() * 2
        self.d = d or py5.random(20, 50)
        self.handedness = h or py5.random_choice((-1, 1))

    def update(self):
        self.display()
        self.move()
        self.d = self.d * 0.985
        if py5.random(100) < 1:
            particles.append(
                Particle(
                    self.pos.x,
                    self.pos.y,
                    self.z,
                    self.d,
                    -self.vel,
                    h=self.handedness,
                )
            )
        if self.d < 1:
            particles.remove(self)

    def display(self):
        py5.no_stroke()
        cor = py5.remap(self.d, 0, DIAMETRO, 0, 255)
        py5.fill(cor, 200)
        with py5.push():
            py5.translate(self.pos.x, self.pos.y, self.z)
            py5.circle(0, 0, self.d)

    def move(self):
        self.pos += self.vel
        self.pos.x %= py5.width
        self.pos.y %= py5.height
        self.vel.rotate(py5.radians(2) * self.handedness)
        self.vel *= 0.99


def _popula_particulas():
    global Z_BASE
    grade: product[tuple[int, ...]] = product(
        range(BORDA, py5.width - BORDA + 1, PASSO), repeat=2
    )
    for xb, yb in grade:
        deslocamento = py5.random_int(-ALEATORIO, ALEATORIO)
        for _ in range(REPETICOES):
            x, y = xb + deslocamento, yb + deslocamento
            particles.append(Particle(x, y, Z_BASE, d=DIAMETRO))
    Z_BASE += 1


def setup():
    global cor_fundo
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.CMAP, "cividis", 255)
    cor_fundo = py5.color(128)
    py5.background(cor_fundo)
    _popula_particulas()


def draw():
    with py5.push():
        py5.translate(0, 0, -10)
        py5.fill(0, 10)
        for p in particles.copy():
            p.update()
    with py5.push():
        py5.translate(0, 0, 0)
        # Credits and go
        canvas.sketch_frame(
            sketch, py5.color(200), "large_transparent_white", "transparent_white"
        )


def key_pressed():
    key = py5.key
    match key:
        case "r":
            _popula_particulas()
        case "c":
            particles.clear()
            py5.background(cor_fundo)
            _popula_particulas()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
