from typing import List

from models.floor_component import FloorComponent
from models.floor_structure_config import FloorStructureConfig
from models.slab import Slab


class BeamComponent(FloorComponent):
    def __init__(self, name: str, color: int, width: float, height: float):
        super().__init__(name, color)
        self.width = width
        self.height = height
        self._ifc_type = "IfcMember"

    def create(self, slab_element: Slab, config: FloorStructureConfig) -> List[int]:
        from cad_adapter.adapter_api_wrappers import create_rectangular_beam, get_element_zl, move_point
        from .beam_geometry import calculate_primary_beam_points

        points_start_edge, points_end_edge = self._create_beam_distribution_points(slab_element, self.width,
                                                                                   config.spacing)

        structure_1_start, structure_1_end = self._calculate_extreme_edge_points(points_start_edge)
        structure_2_start, structure_2_end = self._calculate_extreme_edge_points(points_end_edge)

        beam_ids = []
        for start_pt, end_pt in zip(points_start_edge, points_end_edge):
            beam_ids.append(create_rectangular_beam(start_pt, end_pt,
                                                    self.width,
                                                    self.height,
                                                    get_element_zl(slab_element.element_id)))

        s1_start, s1_end, s2_start, s2_end = calculate_primary_beam_points(
            structure_1_start, structure_1_end, structure_2_start, structure_2_end, self.width)

        beam_id_ref = create_rectangular_beam(s1_start, s1_end, self.width, self.height,
                                              get_element_zl(slab_element.element_id))
        beam_id_op = create_rectangular_beam(s2_start, s2_end, self.width, self.height,
                                             get_element_zl(slab_element.element_id))

        beam_ids.append(beam_id_ref)
        beam_ids.append(beam_id_op)

        self._element_ids = beam_ids
        return beam_ids

    @staticmethod
    def _calculate_extreme_edge_points(edge_points):
        from .geom_utils import calculate_extreme_min_point, calculate_extreme_max_point
        min_point = calculate_extreme_min_point(edge_points)
        max_point = calculate_extreme_max_point(edge_points)
        return min_point, max_point

    @staticmethod
    def _create_beam_distribution_points(slab_element, beam_width, spacing):
        from cad_adapter.adapter_api_wrappers import move_point
        from .geom_utils import normalize_vector, compute_beam_distribution_points

        move_vector_start_edge = slab_element.axis_local_width_direction * -1.
        move_distance = (slab_element.slab_width * .5) - beam_width

        moved_start_point = move_point(slab_element.axis_start_point,
                                       move_vector_start_edge,
                                       move_distance)
        moved_end_point = move_point(slab_element.axis_end_point,
                                     move_vector_start_edge,
                                     move_distance)

        vector_start_to_end = normalize_vector(moved_start_point, moved_end_point)
        moved_start_point = moved_start_point + vector_start_to_end * (beam_width * .5)
        moved_end_point = moved_end_point - vector_start_to_end * (beam_width * .5)

        points_ref_edge = compute_beam_distribution_points(moved_start_point,
                                                           moved_end_point,
                                                           spacing)
        points_ref_edge.append(moved_end_point)
        points_opposite_edge = [move_point(point,
                                           slab_element.axis_local_width_direction,
                                           slab_element.slab_width - beam_width * 2) for point in points_ref_edge]

        return points_ref_edge, points_opposite_edge

    def apply_component_feature(self):
        """Hook... """
        pass