import math
from typing import List, Tuple

import cadwork

from cad_adapter.adapter_api_wrappers import move_point, create_node, create_rectangular_beam, get_element_zl
from .floor_structure_config import FloorStructureConfig
from .slab import map_slab_data, Slab


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

    n_beams = int(length // spacing)
    positions = []

    for i in range(n_beams + 1):
        pos = start_point + (direction * spacing * i)
        positions.append(pos)

    return positions


class FloorStructure:

    def __init__(self, slab_element: int, config: FloorStructureConfig):
        self.slab_element_id = slab_element
        self.config = config
        self.slab_element = map_slab_data(slab_element)

    def generate_beam_distribution_points(self) -> Tuple[List[cadwork.point_3d], List[cadwork.point_3d]]:
        # TODO maybe cleaner to have two separate methods for start and end edge
        points_start_edge, points_end_edge = self._create_beam_distribution_points(self.slab_element,
                                                                                   self.config.beam_config.width)
        print(f"Start edge points: {points_start_edge}")
        print(f"End edge points: {points_end_edge}")
        [create_node(p) for p in [*points_end_edge, *points_start_edge]]

        return points_start_edge, points_end_edge

    @staticmethod
    def calculate_extreme_edge_points(edge_points: List[cadwork.point_3d]) -> Tuple[
        cadwork.point_3d, cadwork.point_3d]:
        min_point = min(edge_points, key=lambda p: (p.x ** 2 + p.y ** 2 + p.z ** 2))
        max_point = max(edge_points, key=lambda p: (p.x ** 2 + p.y ** 2 + p.z ** 2))

        return min_point, max_point

    def create_beam(self, start_point: cadwork.point_3d, end_point: cadwork.point_3d, width: float,
                    height: float) -> int:
        return create_rectangular_beam(start_point, end_point,
                                       width,
                                       height,
                                       get_element_zl(self.slab_element_id))

    def _create_beam_distribution_points(self, slab_element: Slab, beam_width: float):
        move_vector_start_edge = slab_element.axis_local_width_direction * -1.
        move_distance = slab_element.slab_width * .5

        create_node(slab_element.axis_start_point)
        create_node(slab_element.axis_end_point)

        moved_start_point = move_point(slab_element.axis_start_point,
                                       move_vector_start_edge,
                                       move_distance)
        moved_end_point = move_point(slab_element.axis_end_point,
                                     move_vector_start_edge,
                                     move_distance)

        # vector_start_to_end = normalize_vector(moved_end_point, moved_start_point) #TODO
        # moved_start_point = moved_start_point + vector_start_to_end * (beam_width * .5)
        # moved_end_point = moved_end_point + vector_start_to_end * (beam_width * .5)

        points_ref_edge = compute_beam_distribution_points(moved_start_point,
                                                           moved_end_point,
                                                           self.config.spacing)
        points_ref_edge.append(moved_end_point)  # we need to add the last point for the closing beam
        points_opposite_edge = [move_point(point,
                                           slab_element.axis_local_width_direction,
                                           slab_element.slab_width) for point in points_ref_edge]

        return (points_ref_edge, points_opposite_edge)

    def generate_structure(self) -> bool:
        # TODO: Implement the logic to create beams and boards
        return False

    def get_total_volume(self):
        # TODO: Calculate the total volume of the floor structure.
        volume = 0.0

        return volume
