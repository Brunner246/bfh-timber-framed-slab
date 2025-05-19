import math
from typing import List, Tuple

import cadwork

from cad_adapter.adapter_api_wrappers import move_point, create_node, create_rectangular_beam, get_element_zl, \
    get_active_elements, filter_slab_element_id, set_color, set_name, create_rectangular_panel
from .beam_geometry import calculate_primary_beam_points
from .floor_structure_config import FloorStructureConfig, BeamConfig
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

    def _generate_beam_distribution_points(self) -> Tuple[List[cadwork.point_3d], List[cadwork.point_3d]]:
        points_start_edge, points_end_edge = self._create_beam_distribution_points(self._slab_element,
                                                                                   self.config.beam_config.width)
        # TODO visualize the points
        # [create_node(p) for p in [*points_end_edge, *points_start_edge]]
        return points_start_edge, points_end_edge

    @staticmethod
    def _calculate_extreme_edge_points(edge_points: List[cadwork.point_3d]) -> Tuple[
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
        # slab_element_id = self._filter_slab_element_id_from_elements()
        # if slab_element_id is None:
        #     raise ValueError("No valid slab element found.")
        # self.floor_structure = FloorStructure(slab_element_id, config)
        points_start_edge, points_end_edge = self._generate_beam_distribution_points()
        structure_1_start, structure_1_end = self._calculate_extreme_edge_points(points_start_edge)
        structure_2_start, structure_2_end = self._calculate_extreme_edge_points(points_end_edge)

        self._create_beams_with_attributes(config, points_end_edge, points_start_edge,
                                           structure_1_end,
                                           structure_1_start, structure_2_end,
                                           structure_2_start)

        self._create_top_panel_with_attributes(config)
        self._create_bottom_panel_with_attributes(config)

    def get_total_volume(self):
        # TODO: Calculate the total volume of the floor structure.
        volume = 0.0

        return volume

    # @staticmethod
    # def _filter_slab_element_id_from_elements():
    #     elements = get_active_elements()
    #     slab_element_id = filter_slab_element_id(elements)
    #     return slab_element_id

    def _create_bottom_panel_with_attributes(self, config):
        panel_id = self._create_bottom_panel(config)
        set_color([panel_id], config.bottom_panel_config.color)
        set_name([panel_id], config.bottom_panel_config.name)

    def _create_top_panel_with_attributes(self, config):
        panel_id = self._create_top_panel(config)
        set_color([panel_id], config.top_panel_config.color)
        set_name([panel_id], config.top_panel_config.name)

    def _create_top_panel(self, config):
        panel_thickness = config.top_panel_config.thickness
        moved_axis_p1 = move_point(self.slab_element.axis_start_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5)
        moved_axis_p2 = move_point(self.slab_element.axis_end_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5)
        moved_axis_p3 = move_point(self.slab_element.axis_height_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5)
        return create_rectangular_panel(self.slab_element.slab_width,
                                        panel_thickness, moved_axis_p1,
                                        moved_axis_p2,
                                        moved_axis_p3)

    def _create_bottom_panel(self, config):
        panel_thickness = config.bottom_panel_config.thickness
        moved_axis_p1 = move_point(self.slab_element.axis_start_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5 * -1)
        moved_axis_p2 = move_point(self.slab_element.axis_end_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5 * -1)
        moved_axis_p3 = move_point(self.slab_element.axis_height_point,
                                   self.slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + panel_thickness) * .5 * -1)
        return create_rectangular_panel(self.slab_element.slab_width,
                                        panel_thickness, moved_axis_p1,
                                        moved_axis_p2,
                                        moved_axis_p3)

    def _create_beams_with_attributes(self, config, points_end_edge, points_start_edge, structure_1_end,
                                      structure_1_start, structure_2_end, structure_2_start):
        beam_ids = self._create_beam_structure(config, points_end_edge,
                                               points_start_edge,
                                               structure_1_start, structure_1_end,
                                               structure_2_start, structure_2_end)
        set_color(beam_ids, config.beam_config.color)
        set_name(beam_ids, config.beam_config.name)

    def _create_beam_structure(self, config, points_end_edge, points_start_edge,
                               structure_1_start, structure_1_end, structure_2_start, structure_2_end) -> \
            List[int]:
        beam_ids = self._create_secondary_beam_structure(config.beam_config, points_end_edge,
                                                         points_start_edge)

        beam_id_op, beam_id_ref = self._create_primary_beams_structure(config,
                                                                       structure_1_end,
                                                                       structure_1_start,
                                                                       structure_2_end,
                                                                       structure_2_start)
        beam_ids.append(beam_id_ref)
        beam_ids.append(beam_id_op)
        return beam_ids

    def _create_primary_beams_structure(self, config, structure_1_end, structure_1_start, structure_2_end,
                                        structure_2_start):

        s1_start, s1_end, s2_start, s2_end = calculate_primary_beam_points(structure_1_start,
                                                                           structure_1_end,
                                                                           structure_2_start,
                                                                           structure_2_end,
                                                                           config.beam_config.width)

        beam_id_ref = self._create_primary_beam_structure(config.beam_config, s1_start, s1_end)
        beam_id_op = self._create_primary_beam_structure(config.beam_config, s2_start, s2_end)

        return beam_id_op, beam_id_ref

    def _create_primary_beam_structure(self, config: BeamConfig, structure_1_start, structure_2_end) -> int:
        return self.create_beam(structure_1_start, structure_2_end,
                                                config.width,
                                                config.height)

    def _create_secondary_beam_structure(self, config: BeamConfig, points_end_edge, points_start_edge) -> List[int]:
        beam_ids = []
        if len(points_start_edge) != len(points_end_edge):
            raise ValueError("Start and end points must have the same length.")
        for start_pt, end_pt in zip(points_start_edge, points_end_edge):
            beam_ids.append(self.create_beam(start_pt, end_pt,
                                                             config.width,
                                                             config.height))
        return beam_ids
