import numpy as np
import py5


def pontos_circulo(
    total_pontos: int = 360, raio: float = 100.0, x0: float = 0.0, y0: float = 0.0
):
    pontos = []

    for idx in range(total_pontos):
        angulo = 360 / total_pontos * idx
        x = x0 + (np.cos(py5.radians(angulo)) * raio)
        y = y0 + (np.sin(py5.radians(angulo)) * raio)
        pontos.append((x, y))
    return pontos


def pontos_circulo_3d(
    total_pontos: int = 360,
    raio: float = 100.0,
    x0: float = 0.0,
    y0: float = 0.0,
    z0: float = 0.0,
    normal: tuple[int] = (0, 0, 1),
) -> list[tuple[int, int, int]]:
    pontos = []

    # Normalize the normal vector
    normal = np.array(normal)
    normal = normal / np.linalg.norm(normal)

    # Find rotation axis (cross product of Z-axis and normal)
    z_axis = np.array([0, 0, 1])
    rot_axis = np.cross(z_axis, normal)
    rot_angle = np.arccos(np.clip(np.dot(z_axis, normal), -1.0, 1.0))

    # If rotation needed, build the rotation matrix using Rodrigues' formula
    if np.linalg.norm(rot_axis) > 1e-6:
        rot_axis = rot_axis / np.linalg.norm(rot_axis)
        K = np.array(
            [
                [0, -rot_axis[2], rot_axis[1]],
                [rot_axis[2], 0, -rot_axis[0]],
                [-rot_axis[1], rot_axis[0], 0],
            ]
        )
        R = np.eye(3) + np.sin(rot_angle) * K + (1 - np.cos(rot_angle)) * np.dot(K, K)
    else:
        R = np.eye(3)  # No rotation needed (already in XY plane)

    for idx in range(total_pontos):
        angulo = 360 / total_pontos * idx
        x = np.cos(py5.radians(angulo)) * raio
        y = np.sin(py5.radians(angulo)) * raio
        z = 0

        # Rotate point
        point = np.dot(R, np.array([x, y, z]))
        # Translate to center
        point += np.array([x0, y0, z0])

        pontos.append(tuple(point))

    return pontos
