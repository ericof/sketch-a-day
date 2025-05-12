"""2025-05-12
Rotações 05
Grade com rotação de formas geométricas
png
Sketch,py5,CreativeCoding
"""

from collections import defaultdict

import numpy as np
import py5

from padroes import biblioteca as b
from padroes import tipos as t
from padroes.fabrica import GradeLinearPadroes
from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

paletas = [
    gera_paleta("laranja", True),
    gera_paleta("laranja", True),
]


def gera_colecao() -> list[t.Padrao]:
    payload = {"traco": 8}
    padrao_01 = b.Biblioteca.get_padrao("TracosParalelos5")
    padrao_02 = b.Biblioteca.get_padrao("Circulo3Raios")
    colecao = [padrao_01(**payload), padrao_02(**payload)]
    return colecao


padroes = gera_colecao()


def dentro_limites(x: float, y: float, c_x: float, c_y: float, raio: float):
    centro = np.array([c_x, c_y])
    ponto = np.array([x, y])
    distancia = np.sum((ponto - centro) ** 2)
    return distancia <= raio**2


def calcula_rotacao(x: float, y: float, c_x: float, c_y: float):
    dx = x - c_x
    dy = y - c_y
    angulo_rad = np.arctan2(dy, dx)
    angulo = np.degrees(angulo_rad)
    return angulo % 360


def padrao_rotacao(x: float, y: float, c_x: float, c_y: float, raio: float):
    dentro = dentro_limites(x, y, c_x, c_y, raio)
    padrao = padroes[-1] if dentro else padroes[0]
    rotacao = 0 if dentro else calcula_rotacao(x, y, c_x, c_y)
    return padrao, rotacao


def gera_cores_padrao(idy: int, idx: int) -> t.CoresPadrao:
    paleta = paletas[idy % 2]
    traco = paleta[0]
    fundo = py5.color("#000")
    paleta.rotate(idx)
    return t.CoresPadrao(traco, traco, fundo)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    colecao = gera_colecao()
    with py5.push():
        py5.translate(0, 0, -200)
        py5.rect_mode(py5.CORNER)
        py5.fill("#111")
        py5.rect(-py5.width * 2, -py5.height * 2, py5.width * 4, py5.height * 4)
    celulas = 20
    espacamento = 4
    fundo = py5.color("#333")
    borda = t.Borda(fundo, espacamento)
    largura = 800
    meio_largura = largura / 2
    limite_circulos = meio_largura / 3
    imagens = defaultdict(list)
    for idz in range(0, 1):
        grade = GradeLinearPadroes(
            largura,
            largura,
            celulas,
            celulas,
            (espacamento, espacamento),
            colecao,
            borda=borda,
        )
        z = -10
        for celula in grade.celulas:
            idy = celula.idy
            idx = celula.idx
            cores = gera_cores_padrao(idy, idx)
            if idz != 0:
                cores.fundo = None
            padrao, rotacao = padrao_rotacao(
                celula.x, celula.y, meio_largura, meio_largura, limite_circulos
            )
            img = celula(padrao, rotacao * -1, cores, False)
            key = (celula.x, celula.y, z, celula.largura, celula.altura)
            imagens[key].append(img)
    for key, imgs in imagens.items():
        x, y, z, lar, alt = key
        imgs = sum([img.get_np_pixels() for img in imgs])
        img = py5.create_image_from_numpy(imgs.astype(np.uint8))
        with py5.push():
            py5.translate(x, y, z)
            py5.image(img, 0, 0, lar, alt)
    helpers.write_legend(sketch=sketch, frame="#FFF", cor="#000")


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
