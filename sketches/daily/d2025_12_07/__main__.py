"""2025-12-07
Mapas v2: Brasília
Mapa do Sudoeste, Brasília, DF, Brasil.
ericof.com|Poly data (c) OpenStreetMap contributors - https://www.openstreetmap.org/copyright
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.mapas import v2 as mv2

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

FORMA: py5.Py5Shape | None = None
FUNDO = None

zpt = {
    "x": 2197,
    "y": 3326,
    "scale": 1.77146,
    "amount": 0,
}  # zoom & pan transformation values


def escala(geodata: mv2.t.GeoDataV2) -> tuple[float, float, float, float, float, float]:
    x_min, y_min, x_max, y_max = geodata.boundary
    map_w, map_h = (x_max - x_min), (y_max - y_min)
    x_scale, y_scale = py5.width / map_w, py5.height / map_h
    return x_min, y_min, x_max, y_max, x_scale, y_scale


def cria_forma(geodata: mv2.t.GeoDataV2, camadas: dict, caminhos: dict) -> py5.Py5Shape:
    x_min, y_min, x_max, y_max, x_scale, y_scale = escala(geodata)
    forma = py5.create_shape(py5.GROUP)

    for name, camada in camadas.items():
        feature = geodata.features[name]
        gdf = feature.gdf
        paleta = camada["paleta"]
        mv2.translate_and_scale_gdf(gdf, -x_min, -y_min, x_scale, -y_scale)
        for g in gdf.geometry:
            cor = paleta[0]
            py5.fill(cor)
            py5.no_stroke()
            forma.add_child(py5.convert_shape(g))
            paleta.rotate(1)

    for name, camada in caminhos.items():
        feature = geodata.networks[name]
        gdf = feature.gdf
        paleta = camada["paleta"]
        mv2.translate_and_scale_gdf(gdf, -x_min, -y_min, x_scale, -y_scale)
        for g in gdf.geometry:
            cor = paleta[0]
            py5.no_fill()
            py5.stroke(cor)
            forma.add_child(py5.convert_shape(g))
            paleta.rotate(1)
    return forma


def setup():
    global FORMA, FUNDO
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CENTER)
    paleta = gera_paleta("bege-02", True)
    fundo = gera_paleta("bege-01", True)
    FUNDO = fundo.pop()
    py5.background(FUNDO)
    # Inicializa OSMnx
    mv2.d_utils.inicializa_osmnx(log_console=False)
    camadas = {
        "amenity": {"tag": {"amenity": True}, "paleta": paleta},
        "building": {"tag": {"building": True}, "paleta": paleta},
        "water": {"tag": {"water": True}, "paleta": deque(["#6BA6EF"])},
        "green": {
            "tag": {"leisure": ["pitch", "park", "playground"], "landuse": ["grass"]},
            "paleta": deque(["#659565"]),
        },
    }
    caminhos = {
        "roads": {
            "tag": {
                "highway": [
                    "tertiary_link",
                    "secondary",
                    "primary",
                    "track",
                    "turning_circle",
                    "residential",
                    "secondary_link",
                    "living_street",
                    "tertiary",
                    "service",
                    "footway",
                    "primary_link",
                ]
            },
            "paleta": deque(["#000"]),
        },
        "rail": {"tag": {"railway": True}, "paleta": deque(["#585858"])},
    }
    limite = "Sudoeste, Brasília, DF, Brasil"
    endereco = "SQSW 103, Sudoeste, Brasília, DF, Brasil"
    print(f"Obtendo dados OSMnx para {endereco}...")
    geodata = mv2.obtem_dados_osmnx(
        pasta=sketch.path,
        limite=limite,
        endereco=endereco,
        distancia=3000,
        camadas=camadas,
        caminhos=caminhos,
    )
    print(f"Obtendo dados OSMnx para {endereco}... concluído.")
    FORMA = cria_forma(geodata, camadas, caminhos)


def draw():
    global FUNDO
    if FUNDO and FORMA:
        py5.background(FUNDO)
        with py5.push():
            py5.translate(zpt["x"], zpt["y"], -2)
            py5.scale(zpt["scale"])
            FORMA.set_stroke_weight(1 / zpt["scale"])
            py5.shape(FORMA)
    py5.window_title(f"Sketch - Frame {zpt['x'], zpt['y'], zpt['scale']}")
    cor_fundo = py5.color(0)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def mouse_wheel(e):
    xrd = (py5.mouse_x - zpt["x"]) / zpt["scale"]
    yrd = (py5.mouse_y - zpt["y"]) / zpt["scale"]
    zpt["amount"] -= e.get_count()
    zpt["scale"] = 1.1 ** zpt["amount"]
    zpt["x"] = int(py5.mouse_x - xrd * zpt["scale"])
    zpt["y"] = int(py5.mouse_y - yrd * zpt["scale"])


def mouse_dragged():
    zpt["x"] += py5.mouse_x - py5.pmouse_x
    zpt["y"] += py5.mouse_y - py5.pmouse_y


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
