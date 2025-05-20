from abc import abstractmethod
from typing import List, Tuple

import cadwork

from models.floor_component import FloorComponent
from models.floor_structure_config import FloorStructureConfig
from models.slab import Slab


class PanelComponent(FloorComponent):
    def __init__(self, name: str, color: int):
        super().__init__(name, color)

    @abstractmethod
    def get_direction_multiplier(self) -> float:
        """Return the direction multiplier for panel positioning"""
        pass

    @abstractmethod
    def get_ifc_type(self) -> str:
        """Return the IFC type for the panel"""
        pass

    def _calculate_panel_points(self, slab_element, beam_height: float, panel_thickness: float
                                ) -> Tuple[cadwork.point_3d, cadwork.point_3d, cadwork.point_3d]:
        from cad_adapter.adapter_api_wrappers import move_point

        direction_multiplier = self.get_direction_multiplier()
        offset_distance = (beam_height + panel_thickness) * 0.5 * direction_multiplier

        p1 = move_point(
            slab_element.axis_start_point,
            slab_element.axis_local_thickness_direction,
            offset_distance
        )

        p2 = move_point(
            slab_element.axis_end_point,
            slab_element.axis_local_thickness_direction,
            offset_distance
        )

        p3 = move_point(
            slab_element.axis_height_point,
            slab_element.axis_local_thickness_direction,
            offset_distance
        )

        return p1, p2, p3


class TopPanelComponent(PanelComponent):
    def __init__(self, name: str, color: int):
        super().__init__(name, color)

    def get_direction_multiplier(self) -> float:
        return 1.0

    def get_ifc_type(self) -> str:
        return "IfcPlate"

    def create(self, slab_element: Slab, config: FloorStructureConfig) -> List[int]:
        from cad_adapter.adapter_api_wrappers import create_rectangular_panel

        top_panel_points = self._calculate_panel_points(
            slab_element,
            config.beam_config.height,
            config.top_panel_config.thickness
        )

        panel_id = create_rectangular_panel(
            width=slab_element.slab_width,
            thickness=config.top_panel_config.thickness,
            p1=top_panel_points[0],
            p2=top_panel_points[1],
            p3=top_panel_points[2]
        )

        self._element_ids = [panel_id]
        self._ifc_type = self.get_ifc_type()
        return self._element_ids


class BottomPanelComponent(PanelComponent):
    def __init__(self, name: str, color: int):
        super().__init__(name, color)

    def get_direction_multiplier(self) -> float:
        return -1.0

    def get_ifc_type(self) -> str:
        return "IfcCovering"

    def create(self, slab_element: Slab, config: FloorStructureConfig) -> List[int]:
        from cad_adapter.adapter_api_wrappers import create_rectangular_panel

        bottom_panel_points = self._calculate_panel_points(
            slab_element,
            config.beam_config.height,
            config.bottom_panel_config.thickness
        )

        print(f"Bottom panel points: {bottom_panel_points}")

        panel_id = create_rectangular_panel(
            width=slab_element.slab_width,
            thickness=config.bottom_panel_config.thickness,
            p1=bottom_panel_points[0],
            p2=bottom_panel_points[1],
            p3=bottom_panel_points[2]
        )

        self._element_ids = [panel_id]
        self._ifc_type = self.get_ifc_type()
        return self._element_ids
