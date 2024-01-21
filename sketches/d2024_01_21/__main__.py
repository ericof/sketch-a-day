"""2024-01-21
Genuary 21 - New Library.
Escreve #Genuary24 a partir de polígonos Shapely.
png
Sketch,py5,CreativeCoding,genuary,genuary21
"""
import py5
from shapely import Polygon

from utils import helpers

AGRADECIMENTO = """
Possível graças ao exemplo disponível em:
https://github.com/villares/villares/blob/main/shapely_helpers.py
"""

sketch = helpers.info_for_sketch(__file__, __doc__)


def process_glyphs(polys):
    """
    Try to subtract the shapely Polygons representing a glyph
    in order to produce appropriate looking glyphs!
    """
    polys = sorted(polys, key=lambda p: p.area, reverse=True)
    results = [polys[0]]
    for p in polys[1:]:
        # works on edge cases like â and ®
        for i, earlier in enumerate(results):
            if earlier.contains(p):
                results[i] = results[i].difference(p)
                break
        else:  # the for-loop's else only executes after unbroken loops
            results.append(p)
    return results


def polys_from_text(words, font: py5.Py5Font, leading=None, alternate_spacing=False):
    """
    Produce a list of shapely Polygons (with holes!) from a string.
    New-line chars will try to move text to a new line.

    The alternate_spacing option will pick the glyph
    spacing from py5.text_width() for each glyph, it can be
    too spaced, but good for monospaced font alignment.
    """
    leading = leading or font.get_size()
    py5.text_font(font)
    space_width = py5.text_width(" ")
    results = []
    x_offset = y_offset = 0
    for c in words:
        if c == "\n":
            y_offset += leading
            x_offset = 0  # assuming left aligned text...
            continue
        glyph_pt_lists = [[]]
        c_shp = font.get_shape(c, 1)
        vs3 = [c_shp.get_vertex(i) for i in range(c_shp.get_vertex_count())]
        vs = set()
        for vx, vy, _ in vs3:
            x = vx + x_offset
            y = vy + y_offset
            glyph_pt_lists[-1].append((x, y))
            if (x, y) not in vs:
                vs.add((x, y))
            else:
                glyph_pt_lists.append([])  # will leave a trailling empty list

        if alternate_spacing:
            w = py5.text_width(c)
        else:
            w = c_shp.get_width() if vs3 else space_width
        x_offset += w
        # filter out elements with less than 3 points
        # and stop before the trailling empty list
        glyph_polys = [Polygon(p) for p in glyph_pt_lists]
        if glyph_polys:  # there are still empty glyphs at this point
            glyph_shapes = process_glyphs(glyph_polys)
            results.extend(glyph_shapes)
    return results


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    espacamento = 0
    texto = "#Genuary2024"
    fonte = py5.create_font("KonamiWaiWaiWorldFamicomExtended", 30)
    poligonos = polys_from_text(texto, fonte)
    largura = 0
    formas = []
    for poligono in poligonos:
        forma = py5.convert_shape(poligono)
        largura += forma.width
        formas.append((forma, forma.width))
    x = -largura
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        for forma, w in formas:
            py5.shape(forma, x, 0)
            x += w + espacamento
    helpers.write_legend(sketch=sketch)


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
