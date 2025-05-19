from typing import List

from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_id, set_color
from models.floor_structure import FloorStructure
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
            structure_1_start, structure_2_end = self.floor_structure.calculate_extreme_edge_points(points_start_edge)

            beam_ids = self._create_beam_structure(config, points_end_edge, points_start_edge,
                                        structure_1_start, structure_2_end)

            set_color(beam_ids, config.beam_config.color)

            # beams = [self.floor_structure.create_beam(distribution_points) for ]
            return self.floor_structure.generate_structure()
        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

    def _create_beam_structure(self, config, points_end_edge, points_start_edge, structure_1_start, structure_2_end) -> \
    List[int]:
        beam_ids = self._create_secondary_beam_structure(config.beam_config, points_end_edge,
                                                         points_start_edge)
        beam_id = self._create_primary_beam_structure(config.beam_config, structure_1_start,
                                                      structure_2_end)
        beam_ids.append(beam_id)
        return beam_ids

    def _create_primary_beam_structure(self, config: BeamConfig, structure_1_start, structure_2_end) -> int:
        return self.floor_structure.create_beam(structure_1_start, structure_2_end,
                                                config.width,
                                                config.height)

    def _create_secondary_beam_structure(self, config: BeamConfig, points_end_edge, points_start_edge) -> List[int]:
        beam_ids = []
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
