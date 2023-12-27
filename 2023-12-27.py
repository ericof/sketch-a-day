"""2023-12-27

Baseado em https://github.com/viblo/pymunk/blob/master/pymunk/examples/planet.py
"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path
from scipy.spatial import distance

import math
import py5
import pymunk


IMG_NAME = Path(__file__).name.replace(".py", "")

gravityStrength = 5.0e6
space = pymunk.Space()
planetas = (
    (700, 0),
    (-140, 0),
    (-700, 0),
    (140, 0),
)
PLANETAS = []


def gravidade(body, g, damping, dt):
    sq_dist = body.position.get_dist_sqrd((0, 0))
    g = (
        (body.position - pymunk.Vec2d(0, 0))
        * -gravityStrength
        / (sq_dist * math.sqrt(sq_dist))
    )
    pymunk.Body.update_velocity(body, g, damping, dt)


def novo_planeta(space, x, y, cor):
    body = pymunk.Body()
    body.position = pymunk.Vec2d(x, y)
    body.velocity_func = gravidade

    r = body.position.get_distance((0, 0))
    v = math.sqrt(gravityStrength / r) / r
    body.velocity = (body.position - pymunk.Vec2d(0, 0)).perpendicular() * v
    body.angular_velocity = v
    body.angle = math.atan2(body.position.y, body.position.x)

    planet = pymunk.Circle(body, radius=10)
    planet.mass = 1
    planet.friction = 0.7
    planet.elasticity = 0
    planet.color = cor
    space.add(body, planet)
    return planet


def setup():
    global PLANETAS
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    cor = py5.color(0, 0, 255)
    for x, y in planetas:
        PLANETAS.append(novo_planeta(space, x, y, cor))


def draw():
    frame = py5.frame_count
    p1, p2, p3, p4 = PLANETAS
    for idx, (inicio, fim, peso, h, b, center) in enumerate(
        (
            (p1, p2, 2, 300, 100, (420, 420, 0)),
            (p3, p4, 2, 120, 80, (380, 380, 0)),
        )
    ):
        if frame % 7 == idx:
            with py5.push_matrix():
                py5.translate(*center)
                pos0 = (inicio.body.position.x, inicio.body.position.y)
                pos1 = (fim.body.position.x, fim.body.position.y)
                distancia = distance.euclidean(pos0, pos1)
                b = b * py5.random(0.6, 1)
                s = (distancia / 100) * 10
                peso = peso * (1 + (1 / (distancia / 100)))
                cor = (h, s, b)
                py5.stroke(*cor)
                py5.stroke_weight(peso)
                py5.line(*pos0, *pos1)
    space.step(1 / py5.get_frame_rate())
    py5.window_title(f"FR: {py5.get_frame_rate():.1f} | Frame Count: {frame}")
    write_legend([py5.color(360, 0, 100)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
