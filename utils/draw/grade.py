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
):
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
):
    """Cria uma grade retornando também os índices."""
    return _cria_grade(
        largura, altura, margem_x, margem_y, celula_x, celula_y, alternada, True
    )
