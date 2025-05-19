from typing import List

from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_id, set_color, set_name, \
    create_rectangular_panel, move_point
from models.beam_geometry import calculate_primary_beam_points
from models.floor_structure import FloorStructure
from models.floor_structure_config import FloorStructureConfig, BeamConfig


class FloorController:
    def __init__(self):
        self.floor_structure = None
        pass

    def create_floor_structure(self, config: FloorStructureConfig):
        try:
            slab_element_id = self._filter_slab_element_id_from_elements()
            if slab_element_id is None:
                raise ValueError("No valid slab element found.")
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
            self.floor_structure = FloorStructure(slab_element_id, config)
            return self.floor_structure.generate_structure(config)

        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

    # def _create_bottom_panel_with_attributes(self, config):
    #     panel_id = self._create_bottom_panel(config)
    #     set_color([panel_id], config.bottom_panel_config.color)
    #     set_name([panel_id], config.bottom_panel_config.name)
    #
    # def _create_top_panel_with_attributes(self, config):
    #     panel_id = self._create_top_panel(config)
    #     set_color([panel_id], config.top_panel_config.color)
    #     set_name([panel_id], config.top_panel_config.name)
    #
    # def _create_top_panel(self, config):
    #     panel_thickness = config.top_panel_config.thickness
    #     moved_axis_p1 = move_point(self.floor_structure.slab_element.axis_start_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5)
    #     moved_axis_p2 = move_point(self.floor_structure.slab_element.axis_end_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5)
    #     moved_axis_p3 = move_point(self.floor_structure.slab_element.axis_height_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5)
    #     return create_rectangular_panel(self.floor_structure.slab_element.slab_width,
    #                                     panel_thickness, moved_axis_p1,
    #                                     moved_axis_p2,
    #                                     moved_axis_p3)
    #
    # def _create_bottom_panel(self, config):
    #     panel_thickness = config.bottom_panel_config.thickness
    #     moved_axis_p1 = move_point(self.floor_structure.slab_element.axis_start_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5 * -1)
    #     moved_axis_p2 = move_point(self.floor_structure.slab_element.axis_end_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5 * -1)
    #     moved_axis_p3 = move_point(self.floor_structure.slab_element.axis_height_point,
    #                                self.floor_structure.slab_element.axis_local_thickness_direction,
    #                                (config.beam_config.height + panel_thickness) * .5 * -1)
    #     return create_rectangular_panel(self.floor_structure.slab_element.slab_width,
    #                                     panel_thickness, moved_axis_p1,
    #                                     moved_axis_p2,
    #                                     moved_axis_p3)
    #
    # def _create_beams_with_attributes(self, config, points_end_edge, points_start_edge, structure_1_end,
    #                                   structure_1_start, structure_2_end, structure_2_start):
    #     beam_ids = self._create_beam_structure(config, points_end_edge,
    #                                            points_start_edge,
    #                                            structure_1_start, structure_1_end,
    #                                            structure_2_start, structure_2_end)
    #     set_color(beam_ids, config.beam_config.color)
    #     set_name(beam_ids, config.beam_config.name)
    #
    # def _create_beam_structure(self, config, points_end_edge, points_start_edge,
    #                            structure_1_start, structure_1_end, structure_2_start, structure_2_end) -> \
    #         List[int]:
    #     beam_ids = self._create_secondary_beam_structure(config.beam_config, points_end_edge,
    #                                                      points_start_edge)
    #
    #     beam_id_op, beam_id_ref = self._create_primary_beams_structure(config,
    #                                                                    structure_1_end,
    #                                                                    structure_1_start,
    #                                                                    structure_2_end,
    #                                                                    structure_2_start)
    #     beam_ids.append(beam_id_ref)
    #     beam_ids.append(beam_id_op)
    #     return beam_ids
    #
    # def _create_primary_beams_structure(self, config, structure_1_end, structure_1_start, structure_2_end,
    #                                     structure_2_start):
    #
    #     s1_start, s1_end, s2_start, s2_end = calculate_primary_beam_points(structure_1_start,
    #                                                                        structure_1_end,
    #                                                                        structure_2_start,
    #                                                                        structure_2_end,
    #                                                                        config.beam_config.width)
    #
    #     beam_id_ref = self._create_primary_beam_structure(config.beam_config, s1_start, s1_end)
    #     beam_id_op = self._create_primary_beam_structure(config.beam_config, s2_start, s2_end)
    #
    #     return beam_id_op, beam_id_ref
    #
    # def _create_primary_beam_structure(self, config: BeamConfig, structure_1_start, structure_2_end) -> int:
    #     return self.floor_structure.create_beam(structure_1_start, structure_2_end,
    #                                             config.width,
    #                                             config.height)
    #
    # def _create_secondary_beam_structure(self, config: BeamConfig, points_end_edge, points_start_edge) -> List[int]:
    #     beam_ids = []
    #     if len(points_start_edge) != len(points_end_edge):
    #         raise ValueError("Start and end points must have the same length.")
    #     for start_pt, end_pt in zip(points_start_edge, points_end_edge):
    #         beam_ids.append(self.floor_structure.create_beam(start_pt, end_pt,
    #                                                          config.width,
    #                                                          config.height))
    #     return beam_ids

    @staticmethod
    def _filter_slab_element_id_from_elements():
        elements = get_active_elements()
        slab_element_id = filter_slab_element_id(elements)
        return slab_element_id
