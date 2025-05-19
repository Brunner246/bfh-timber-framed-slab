from typing import List

import cadwork
import math


def is_normalized(vec: cadwork.point_3d, tol=1e-6):
    coords = [vec.x, vec.y, vec.z]
    length = math.sqrt(sum(x ** 2 for x in coords))
    return abs(length - 1.0) < tol


def interpolate(p1: cadwork.point_3d, p2: cadwork.point_3d, t):
    x = p1.x + t * (p2.x - p1.x)
    y = p1.y + t * (p2.y - p1.y)
    z = p1.z + t * (p2.z - p1.z)
    return cadwork.point_3d(x, y, z)


def vector_length(p1: cadwork.point_3d, p2: cadwork.point_3d) -> float:
    return p1.distance(p2)


def normalize_vector(p1: cadwork.point_3d, p2: cadwork.point_3d) -> cadwork.point_3d:
    length = vector_length(p1, p2)
    if length == 0:
        raise ValueError("Cannot normalize a zero-length vector")
    return cadwork.point_3d((p2.x - p1.x) / length, (p2.y - p1.y) / length, (p2.z - p1.z) / length)


def compute_beam_distribution_points(start_point: cadwork.point_3d, end_point: cadwork.point_3d,
                                     spacing: float) -> List[cadwork.point_3d]:
    length = vector_length(start_point, end_point)
    direction = normalize_vector(start_point, end_point)
    print(f"Direction: {direction} {__name__}")

    n_beams = int(length // spacing)
    positions = []

    for i in range(n_beams + 1):
        pos = start_point + (direction * spacing * i)
        positions.append(pos)

    return positions

def calculate_extreme_min_point(points: List[cadwork.point_3d]) -> cadwork.point_3d:
    return min(points, key=lambda p: (p.x ** 2 + p.y ** 2 + p.z ** 2))

def calculate_extreme_max_point(points: List[cadwork.point_3d]) -> cadwork.point_3d:
    return max(points, key=lambda p: (p.x ** 2 + p.y ** 2 + p.z ** 2))

