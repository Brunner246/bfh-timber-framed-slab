from typing import List

import cadwork

from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_id, set_color, set_name, \
    create_node
from models.floor_structure import FloorStructure, normalize_vector
from models.floor_structure_config import FloorStructureConfig, BeamConfig


class FloorController:
    def __init__(self):
        self.floor_structure = None

    def create_floor_structure(self, config: FloorStructureConfig):
        try:
            slab_element_id = self._filter_slab_element_id_from_elements()
            if slab_element_id is None:
                raise ValueError("No valid slab element found.")
            self.floor_structure = FloorStructure(slab_element_id, config)
            points_start_edge, points_end_edge = self.floor_structure.generate_beam_distribution_points()
            structure_1_start, structure_1_end = self.floor_structure.calculate_extreme_edge_points(points_start_edge)
            structure_2_start, structure_2_end = self.floor_structure.calculate_extreme_edge_points(points_end_edge)

            self._create_beams_with_attributes(config, points_end_edge, points_start_edge,
                                               structure_1_end,
                                               structure_1_start, structure_2_end,
                                               structure_2_start)

            return self.floor_structure.generate_structure()
        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

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
        direction_vector_length: cadwork.point_3d = normalize_vector(structure_1_end, structure_1_start)
        direction_vector_width: cadwork.point_3d = normalize_vector(structure_2_end, structure_1_end)
        structure_2_start += direction_vector_length * config.beam_config.width * .5
        structure_2_end -= direction_vector_length * config.beam_config.width * .5
        structure_2_start -= direction_vector_width * config.beam_config.width * .5
        structure_2_end -= direction_vector_width * config.beam_config.width * .5

        structure_1_start += direction_vector_length * config.beam_config.width * .5
        structure_1_end -= direction_vector_length * config.beam_config.width * .5
        structure_1_start += direction_vector_width * config.beam_config.width * .5
        structure_1_end += direction_vector_width * config.beam_config.width * .5


        # structure_1_end += direction_vector_length * config.beam_config.width
        # move_vector_pos = direction_vector_length * config.beam_config.width * .5
        # move_vector_pos = move_vector_pos + direction_vector_width * config.beam_config.width * .5 * -1.
        # move_vector_neg = direction_vector_length * config.beam_config.width * -1 * .5
        # move_vector_neg = move_vector_neg + direction_vector_width * config.beam_config.width * .5
        # print(f"{move_vector_pos=}")
        # print(f"{move_vector_neg=}")
        # create_node(structure_1_start + move_vector_pos * -1.)
        # create_node(structure_2_start + move_vector_pos)
        beam_id_ref = self._create_primary_beam_structure(config.beam_config,
                                                          structure_1_start,  # + move_vector_pos * -1.,
                                                          structure_1_end)  # ,# + move_vector_pos * -1.)
        beam_id_op = self._create_primary_beam_structure(config.beam_config,
                                                         structure_2_start,  # + move_vector_pos,
                                                         structure_2_end)  # + move_vector_pos)
        return beam_id_op, beam_id_ref

    def _create_primary_beam_structure(self, config: BeamConfig, structure_1_start, structure_2_end) -> int:
        return self.floor_structure.create_beam(structure_1_start, structure_2_end,
                                                config.width,
                                                config.height)

    def _create_secondary_beam_structure(self, config: BeamConfig, points_end_edge, points_start_edge) -> List[int]:
        beam_ids = []
        if len(points_start_edge) != len(points_end_edge):
            raise ValueError("Start and end points must have the same length.")
        for start_pt, end_pt in zip(points_start_edge, points_end_edge):
            beam_ids.append(self.floor_structure.create_beam(start_pt, end_pt,
                                                             config.width,
                                                             config.height))
        return beam_ids

    @staticmethod
    def _filter_slab_element_id_from_elements():
        elements = get_active_elements()
        slab_element_id = filter_slab_element_id(elements)
        return slab_element_id
