import numpy as np


def _cria_grade(
    largura: int,
    altura: int,
    margem_x: int,
    margem_y: int,
    celula_x: int,
    celula_y: int,
    alternada: bool = True,
    indices: bool = False,
):
    """Cria uma grade."""
    pontos = []
    celula_x = int(celula_x)
    celula_y = int(celula_y)
    yi = margem_y
    yf = altura - margem_y
    for idy, y in enumerate(range(yi, yf, celula_y)):
        if (y + celula_y) > yf:
            break
        buffer = int(celula_x / 2) if (alternada and idy % 2) else 0
        xi = margem_x - buffer
        xf = largura - margem_x
        for idx, x in enumerate(range(xi, xf, celula_x)):
            if indices:
                pontos.append((idx, x, idy, y))
            else:
                pontos.append((x, y))
    return pontos


def cria_grade(
    largura: int,
    altura: int,
    margem_x: int,
    margem_y: int,
    celula_x: int,
    celula_y: int,
    alternada: bool = True,
) -> list[tuple[float, float]]:
    """Cria uma grade."""
    return _cria_grade(
        largura, altura, margem_x, margem_y, celula_x, celula_y, alternada, False
    )


def cria_grade_ex(
    largura: int,
    altura: int,
    margem_x: int,
    margem_y: int,
    celula_x: int,
    celula_y: int,
    alternada: bool = True,
) -> list[tuple[int, float, int, float]]:
    """Cria uma grade retornando também os índices."""
    return _cria_grade(
        largura, altura, margem_x, margem_y, celula_x, celula_y, alternada, True
    )


def grade_desigual(
    largura: int,
    altura: int,
    area_min: int,
    area_max: int,
    razao_max: float = 4.0,
    multiplicador_area_max: float = 10.0,
) -> np.ndarray:
    """Cria uma grade com retângulos de tamanhos variados.

    Restrições:
    - área entre area_min e area_max
    - razão entre os lados ≤ razao_max
    - área máxima ≤ multiplicador_area_max × menor área encontrada
    - evita retângulos colados com outro por uma borda inteira
    - todos os pixels são usados
    """
    rng = np.random.default_rng()
    usados = np.zeros((altura, largura), dtype=bool)
    retangulos = []
    menor_area_vista = None

    def nao_usado(x, y, w, h):
        return (
            x + w <= largura
            and y + h <= altura
            and not usados[y : y + h, x : x + w].any()
        )

    def marca_usado(x, y, w, h):
        usados[y : y + h, x : x + w] = True

    def tem_borda_colada(x, y, w, h):
        """Evita retângulos colados em outro por uma borda inteira"""
        if y > 0 and usados[y - 1, x : x + w].all():
            return True
        if y + h < altura and usados[y + h, x : x + w].all():
            return True
        if x > 0 and usados[y : y + h, x - 1].all():
            return True
        if x + w < largura and usados[y : y + h, x + w].all():
            return True
        return False

    for _ in range(100_000):
        x = rng.integers(0, largura)
        y = rng.integers(0, altura)

        if usados[y, x]:
            continue

        l_max = largura - x
        a_max = altura - y

        if l_max <= 0 or a_max <= 0:
            continue

        ret_l = rng.integers(1, l_max + 1)
        ret_a = rng.integers(1, a_max + 1)
        area = ret_l * ret_a

        if area < area_min or area > area_max:
            continue

        razao = max(ret_l / ret_a, ret_a / ret_l)
        if razao > razao_max:
            continue

        if menor_area_vista is None:
            menor_area_vista = area
        elif area > multiplicador_area_max * menor_area_vista:
            continue

        if nao_usado(x, y, ret_l, ret_a) and not tem_borda_colada(x, y, ret_l, ret_a):
            retangulos.append((x, y, ret_l, ret_a))
            marca_usado(x, y, ret_l, ret_a)
            menor_area_vista = min(menor_area_vista, area)

    # Preenche espaços restantes com retângulos menores, sem restrições
    visitados = np.zeros_like(usados)
    for y in range(altura):
        for x in range(largura):
            if not usados[y, x] and not visitados[y, x]:
                w = 1
                while (
                    x + w < largura and not usados[y, x + w] and not visitados[y, x + w]
                ):
                    w += 1

                h = 1
                while (
                    y + h < altura
                    and not usados[y + h, x : x + w].any()
                    and not visitados[y + h, x : x + w].any()
                ):
                    h += 1

                visitados[y : y + h, x : x + w] = True
                retangulos.append((x, y, w, h))

    return np.array(retangulos)
