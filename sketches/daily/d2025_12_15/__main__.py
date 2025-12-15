"""2025-12-15
Particles 08
Sistema de partículas dinâmico com divisão e movimento giratório.
ericof.com|https://abav.lugaralgum.com/sketch-a-day/#sketch_2025_12_03
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

particles = []

BORDA: int = 0
PASSO: int = 240
IDX: int = 0
DIAMETRO: float = 34.0
DDX: float = 0.992
REPETICOES: int = 12
Z_BASE: int = -50


class Particle:
    def __init__(self, x, y, z, d=None, v=None, h=None, paleta=""):
        self.pos = py5.Py5Vector(x, y)
        self.z = z
        self.vel = v or py5.Py5Vector2D.random() * 2
        self.d = d or py5.random(20, 50)
        self.handedness = h or py5.random_choice((-1, 1))
        self.paleta = paleta

    def update(self):
        self.display()
        self.move()
        self.d = self.d * DDX
        if py5.random(100) < 2:
            particles.append(
                Particle(
                    self.pos.x,
                    self.pos.y,
                    self.z,
                    self.d,
                    -self.vel,
                    h=self.handedness,
                    paleta=self.paleta,
                )
            )
        if self.d < 1:
            particles.remove(self)

    def display(self):
        with py5.push():
            py5.color_mode(py5.CMAP, self.paleta, 255)
            py5.no_stroke()
            cor = py5.remap(self.d, 0, DIAMETRO, 0, 255)
            b = py5.random_int(200, 205)
            py5.fill(cor, b)
            py5.translate(self.pos.x, self.pos.y, self.z)
            py5.circle(0, 0, self.d)

    def move(self):
        self.pos += self.vel
        self.pos.x %= py5.width
        self.pos.y %= py5.height
        self.vel.rotate(py5.radians(2) * self.handedness)
        self.vel *= 0.995


def _popula_particulas():
    global IDX, Z_BASE
    grade = cria_grade_ex(
        largura=py5.width,
        altura=py5.height,
        margem_x=0,
        margem_y=0,
        celula_x=PASSO,
        celula_y=PASSO,
        alternada=True,
    )
    for item in grade:
        xb, yb = item[1], item[3]
        paleta = py5.random_choice(("cividis", "viridis", "plasma", "magma"))
        x = xb + (PASSO // 2) * IDX
        y = yb + (PASSO // 2) * IDX
        for _ in range(REPETICOES):
            particles.append(Particle(x, y, Z_BASE, d=DIAMETRO, paleta=paleta))
    Z_BASE += 10
    IDX += 1


def setup():
    global cor_fundo
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.CMAP, "cividis", 255)
    cor_fundo = py5.color(140)
    py5.background(cor_fundo)
    _popula_particulas()


def draw():
    with py5.push():
        py5.translate(0, 0, -80)
        py5.fill(0, 10)
        for p in particles.copy():
            p.update()
    with py5.push():
        py5.color_mode(py5.RGB)
        py5.translate(0, 0, 0)
        py5.no_stroke()
        # Credits and go
        canvas.sketch_frame(
            sketch,
            py5.color(0, 0, 0, 1),
            "large_transparent_white",
            "transparent_white",
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
