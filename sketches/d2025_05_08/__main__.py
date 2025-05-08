"""2025-05-08
Rotações 01
Grade com rotação de forma geométrica
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

paleta = gera_paleta("oliver-13", True)


def gera_colecao() -> list[t.Padrao]:
    payload = {"traco": 8}
    padrao = b.Biblioteca.get_padrao("Quadrado3Raios")
    colecao = [padrao(**payload)]
    return colecao


def gera_cores_padrao(idx: int) -> t.CoresPadrao:
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
        py5.fill("#333")
        py5.rect(-py5.width * 2, -py5.height * 2, py5.width * 4, py5.height * 4)
    celulas = 20
    espacamento = 1
    fundo = py5.color("#111")
    borda = t.Borda(fundo, espacamento)
    largura = 800
    imagens = defaultdict(list)
    passo_y = 15
    passo_x = passo_y / celulas
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
        grade_padroes = grade.padroes
        z = -10
        for celula in grade.celulas:
            idy = celula.idy
            idx = celula.idx
            cores = gera_cores_padrao(idx)
            if idz != 0:
                cores.fundo = None
            padrao = next(grade_padroes)
            rotacao = -(idy * passo_y + idx * passo_x)
            img = celula(padrao, rotacao, cores, False)
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
