"""2024-01-19
Genuary 19 - Flocking
Simulação de 3 tipos de pássaros se agrupando e voando em conjunto.
gif
Sketch,py5,CreativeCoding,genuary,genuary19
"""
from collections import deque
from typing import List

import numpy as np
import py5
import py5_tools
import pymunk

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


space = pymunk.Space()

# Configuracao
DISTANCIA_VIZINHOS = 80
PESO_ALINHAMENTO = 0.2
PESO_COESAO = 0.1
DISTANCIA_SEPARACAO = 10
PESO_SEPARACAO = 8
FORCA_MAX_SEPARACAO = 1
AMORTECIMENTO_SEPARACAO = 0.5
VELOCIDADE_MAX = 6.0


GRUPOS = [
    [[], 40, 20, (255, 0, 0)],
    [[], 100, 10, (100, 255, 0)],
    [[], 80, 9, (0, 0, 220)],
]


class Passaro:
    def __init__(self, posicao, cor, tamanho):
        self.historico = deque(maxlen=10)
        self.historico.append(posicao)
        self.posicao = posicao
        self.velocidade = pymunk.Vec2d(
            np.random.uniform(-1, 1), np.random.uniform(-1, 1)
        )
        self.velocidade_max = VELOCIDADE_MAX
        self.cor = cor
        self.tamanho = tamanho
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.posicao = posicao
        self.body = body
        space.add(body)

    def alinhamento(self, vizinhos: List["Passaro"]):
        if not vizinhos:
            return

        velocidade_med = pymunk.Vec2d(0, 0)
        for vizinho in vizinhos:
            velocidade_med += vizinho.velocidade

        velocidade_med /= len(vizinhos)
        self.velocidade += (velocidade_med - self.velocidade) * PESO_ALINHAMENTO

    def coesao(self, vizinhos: List["Passaro"]):
        if not vizinhos:
            return

        posicao_med = pymunk.Vec2d(0, 0)
        for vizinho in vizinhos:
            posicao_med += vizinho.posicao

        posicao_med /= len(vizinhos)
        cohesion_force = posicao_med - self.posicao
        self.velocidade += cohesion_force * PESO_COESAO

    def separacao(self, vizinhos: List["Passaro"]):
        if not vizinhos:
            return

        direcao = pymunk.Vec2d(0, 0)
        for vizinho in vizinhos:
            distancia = self.posicao.get_distance(vizinho.posicao)
            if 0 < distancia < DISTANCIA_SEPARACAO:
                diff = (self.posicao - vizinho.posicao) / distancia
                direcao += diff

        direcao = direcao.normalized() * FORCA_MAX_SEPARACAO
        direcao *= AMORTECIMENTO_SEPARACAO
        self.velocidade += direcao * PESO_SEPARACAO
        self.velocidade = self.velocidade.normalized() * self.velocidade_max

    def calcula_posicao(self, vizinhos: List["Passaro"]):
        self.alinhamento(vizinhos)
        self.coesao(vizinhos)
        self.separacao(vizinhos)
        self.posicao += self.velocidade
        self.ajusta_limites()
        self.historico.append(self.posicao)

    def desenha(self):
        r, g, b = self.cor
        cor = py5.color(r, g, b, 100)
        py5.fill(cor)
        py5.circle(self.posicao.x, self.posicao.y, self.tamanho)
        total = len(self.historico)
        cor = py5.color(r, g, b, 30)
        for idx, posicao in enumerate(self.historico):
            tamanho = (idx / total) * self.tamanho
            py5.stroke(cor)
            py5.stroke_weight(tamanho)
            py5.point(posicao.x, posicao.y)

    def ajusta_limites(self):
        x = self.posicao.x % py5.width
        y = self.posicao.y % py5.height
        self.posicao = pymunk.Vec2d(x, y)


def encontra_vizinhos(passaro, todos_passaros, range):
    vizinhos = []
    for outro in todos_passaros:
        if outro != passaro and passaro.posicao.get_distance(outro.posicao) < range:
            vizinhos.append(outro)
    return vizinhos


def setup():
    global GRUPOS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    for grupo, numero, tamanho, cor in GRUPOS:
        for _ in range(numero):
            posicao = pymunk.Vec2d(
                np.random.uniform(0, py5.width), np.random.uniform(0, py5.height)
            )
            passaro = Passaro(
                posicao,
                cor=cor,
                tamanho=tamanho,
            )
            grupo.append(passaro)


def draw():
    py5.background(0)
    for grupo, *_ in GRUPOS:
        for passaro in grupo:
            vizinhos = encontra_vizinhos(passaro, grupo, DISTANCIA_VIZINHOS)
            passaro.calcula_posicao(vizinhos)
            passaro.desenha()
    space.step(1 / py5.get_frame_rate())
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
        count=60,
        period=0.25,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
