from contextlib import contextmanager


@contextmanager
def title(title: str):
    """Context manager para atualizar o título da janela durante um processo.

    :param title: Título a ser exibido durante o processo.
    """
    import py5

    py5.window_title(f"Iniciando: {title}")
    yield
    py5.window_title(f"Finalizado: {title}")
