"""2026-02-26
Eyes Collective 05
Desenho que se assemelha a um coletivo de olhos alienígenas
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.esfera import pontos_esfera
from sketches.utils.draw.esfera import vizinhos_knn_esfera
from sketches.utils.draw.olho import Olho
from sketches.utils.helpers import recursos
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.timing import report_time

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

status = True

perimetro = 1000
perimetro_pontos = 1000
outer_r = 600
esfera_raio = outer_r / 8.0

z_factor = 0.05
num_vizinhos = 8


@dataclass
class EsferaInfo:
    esfera: py5.Py5Shape
    x: float
    y: float
    z: float
    rotacoes: list[float]
    controle: list[float]
    escala: float = 1
    vizinhos: list | None = None


esferas: list[EsferaInfo] = []

luz_x = 500
luz_y = 500
luz_z = -1200
brilho = 5
escala = 0.25
fator_escala = 0.25


def cria_esfera(
    textura: py5.Py5Graphics | py5.Py5Image, raio: float, rotacoes: list[float]
) -> py5.Py5Shape:
    esfera = py5.create_shape(py5.SPHERE, raio)
    esfera.set_texture(textura)
    esfera.set_texture_mode(py5.IMAGE)
    esfera.set_stroke(False)
    esfera.rotate_x(py5.radians(rotacoes[0]))
    esfera.rotate_y(py5.radians(rotacoes[1]))
    esfera.rotate_z(py5.radians(rotacoes[2]))
    return esfera


def desenha_olho(info: EsferaInfo):
    esfera = info.esfera
    esfera.set_shininess(brilho)
    if escala != info.escala:
        info.escala *= fator_escala
        esfera.scale(fator_escala)
    x, y, z = info.x, info.y, info.z
    base = info.rotacoes
    controle = info.controle
    with py5.push():
        py5.translate(x, y, z)
        for idx, method in enumerate((
            py5.rotate_x,
            py5.rotate_y,
            py5.rotate_z,
        )):
            rot_base = base[idx]
            valor = controle[idx]
            rotacao = valor - rot_base
            if int(rotacao) != 0:
                method(float(py5.radians(rotacao)))
        py5.shape(esfera)


def desenha_nervo(info: EsferaInfo):
    # pass
    x, y, z = info.x, info.y, info.z
    with py5.push():
        for nx, ny, nz in info.vizinhos:
            py5.stroke(255, 0, 0, 50)
            py5.stroke_weight(1)
            py5.line(x, y, z, nx, ny, nz)


def calcula_coordenadas(xb: float, yb: float, zb: float) -> tuple[float, float, float]:
    mult = py5.random(1 - z_factor, 1 + z_factor)
    return xb, yb, zb * mult


def bagunca_pontos(pontos: tuple[tuple[float, float, float], ...]):
    """Leve bagunçada nos pontos de uma esfera."""
    resultado = []
    for xb, yb, zb in pontos:
        resultado.append(calcula_coordenadas(xb, yb, zb))
    return np.array(resultado)


def setup():
    global esfera_central
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.image_mode(py5.CENTER)
    filename = f"{sketch.day}_pg.png"

    esfera_info = []
    rotacoes = [0.0, 90.0, 0.0]
    pontos = bagunca_pontos(pontos_esfera(perimetro, perimetro_pontos))
    for idx, (x, y, z) in enumerate(pontos):
        vizinhos = [
            tuple(pontos[i]) for i in vizinhos_knn_esfera(pontos, idx, k=num_vizinhos)
        ]
        esfera_info.append((x, y, z, rotacoes[:], vizinhos))

    if not (pg := recursos.carrega_imagem_cache(filename)):
        olho = Olho(
            cores={
                "particulas": py5.color(20, 100, 255),
                "area_central_01": py5.color(15, 50, 20, 50),
                "area_central_02": py5.color(20, 20, 20),
                "anel_interno_01": py5.color(247, 127, 0),
                "anel_interno_02": py5.color(255, 255, 255),
                "anel_central_01": py5.color(0, 255, 167),
                "anel_central_02": py5.color(255, 255, 255),
                "anel_externo_01": py5.color(80, 90, 51),
                "anel_externo_02": py5.color(80, 95, 17),
                "fundo_imagem": py5.color(255, 255, 255),
            }
        )
        pg = olho()
        recursos.salva_imagem_cache(pg, filename)
    with report_time("Cria Esferas"):
        for x, y, z, rotacoes, vizinhos in esfera_info:
            base = rotacoes[:]
            esfera = cria_esfera(pg, esfera_raio, base)
            esferas.append(EsferaInfo(esfera, x, y, z, base, rotacoes, 1.0, vizinhos))

    esfera_central = py5.create_shape(py5.SPHERE, perimetro * (1 - z_factor) * 0.75)
    esfera_central.set_stroke(False)
    # esfera_central.set_fill("#222222")
    esfera_central.set_texture(pg)
    esfera_central.rotate_y(py5.radians(90))


def draw():
    global luz_x, luz_y, fator_escala, escala
    centro = helpers.DIMENSOES.centro
    py5.background(cor_fundo)
    py5.directional_light(200, 200, 200, luz_x, luz_y, luz_z)
    escala *= fator_escala
    with py5.push():
        py5.translate(*centro, -perimetro * 1.5)
        py5.shape(esfera_central)
        # Primeiro desenhamos todas as conexões
        for info in esferas:
            desenha_nervo(info)
        # E depois todos os olhos
        for info in esferas:
            desenha_olho(info)
    # Reseta escala
    fator_escala = 1.0
    texto = (
        f"Frame: {py5.frame_count} - Luz: ({luz_x}, {luz_y}, {luz_z}) - "
        f"Brilho: {brilho} - Escala: {escala:.2f}"
    )
    py5.window_title(texto)

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )
    if not status:
        save_and_close()


def mouse_pressed():
    global luz_x, luz_y
    button = py5.mouse_button
    match button:
        case py5.LEFT:
            luz_x, luz_y = py5.mouse_x, py5.mouse_y


def key_pressed():
    global luz_z, brilho, fator_escala
    key = py5.key
    match key:
        case "r":
            luz_z -= 10
        case "f":
            luz_z += 10
        case "w":
            brilho += 1
        case "s":
            brilho -= 1
        case "a":
            fator_escala = 0.95
        case "d":
            fator_escala = 1.05
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
