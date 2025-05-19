import math
from typing import List, Tuple

import cadwork

from cad_adapter.adapter_api_wrappers import move_point, create_node, create_rectangular_beam, get_element_zl
from .floor_structure_config import FloorStructureConfig
from .geom_utils import calculate_extreme_min_point, calculate_extreme_max_point, normalize_vector, \
    compute_beam_distribution_points
from .slab import map_slab_data, Slab


class FloorStructure:

    def __init__(self, slab_element: int, config: FloorStructureConfig):
        self.slab_element_id = slab_element
        self.config = config
        self._slab_element = map_slab_data(slab_element)

    @property
    def slab_element(self) -> Slab:
        return self._slab_element

    def generate_beam_distribution_points(self) -> Tuple[List[cadwork.point_3d], List[cadwork.point_3d]]:
        points_start_edge, points_end_edge = self._create_beam_distribution_points(self._slab_element,
                                                                                   self.config.beam_config.width)
        # TODO visualize the points
        # [create_node(p) for p in [*points_end_edge, *points_start_edge]]
        return points_start_edge, points_end_edge

    @staticmethod
    def calculate_extreme_edge_points(edge_points: List[cadwork.point_3d]) -> Tuple[
        cadwork.point_3d, cadwork.point_3d]:
        min_point = calculate_extreme_min_point(edge_points)
        max_point = calculate_extreme_max_point(edge_points)

        return min_point, max_point

    def create_beam(self, start_point: cadwork.point_3d, end_point: cadwork.point_3d, width: float,
                    height: float) -> int:
        return create_rectangular_beam(start_point, end_point,
                                       width,
                                       height,
                                       get_element_zl(self.slab_element_id))

    def _create_beam_distribution_points(self, slab_element: Slab, beam_width: float):
        move_vector_start_edge = slab_element.axis_local_width_direction * -1.
        move_distance = (slab_element.slab_width * .5) - beam_width

        moved_start_point = move_point(slab_element.axis_start_point,
                                       move_vector_start_edge,
                                       move_distance)
        moved_end_point = move_point(slab_element.axis_end_point,
                                     move_vector_start_edge,
                                     move_distance)

        vector_start_to_end = normalize_vector(moved_start_point, moved_end_point)
        print(f"Vector start to end: {vector_start_to_end}")
        moved_start_point: cadwork.point_3d = moved_start_point + vector_start_to_end * (beam_width * .5)
        moved_end_point: cadwork.point_3d = moved_end_point - vector_start_to_end * (beam_width * .5)

        points_ref_edge = compute_beam_distribution_points(moved_start_point,
                                                           moved_end_point,
                                                           self.config.spacing)
        points_ref_edge.append(moved_end_point)  # we need to add the last point for the closing beam
        points_opposite_edge = [move_point(point,
                                           slab_element.axis_local_width_direction,
                                           slab_element.slab_width - beam_width * 2) for point in points_ref_edge]

        return points_ref_edge, points_opposite_edge

    def generate_structure(self, config: FloorStructureConfig) -> bool:
        pass
        # slab_element_id = self._filter_slab_element_id_from_elements()
        # if slab_element_id is None:
        #     raise ValueError("No valid slab element found.")
        # self.floor_structure = FloorStructure(slab_element_id, config)
        # points_start_edge, points_end_edge = self.floor_structure.generate_beam_distribution_points()
        # structure_1_start, structure_1_end = self.floor_structure.calculate_extreme_edge_points(points_start_edge)
        # structure_2_start, structure_2_end = self.floor_structure.calculate_extreme_edge_points(points_end_edge)
        #
        # self._create_beams_with_attributes(config, points_end_edge, points_start_edge,
        #                                    structure_1_end,
        #                                    structure_1_start, structure_2_end,
        #                                    structure_2_start)
        #
        # self._create_top_panel_with_attributes(config)
        # self._create_bottom_panel_with_attributes(config)

    def get_total_volume(self):
        # TODO: Calculate the total volume of the floor structure.
        volume = 0.0

        return volume
