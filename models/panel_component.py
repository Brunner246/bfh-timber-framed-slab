from typing import List

from models.floor_component import FloorComponent


class PanelComponent(FloorComponent):
    def __init__(self, name: str, color: int, thickness: float, is_top: bool):
        super().__init__(name, color)
        self.thickness = thickness
        self.is_top = is_top
        self._ifc_type = "IfcPlate" if is_top else "IfcCovering"

    def create(self, slab_element, config) -> List[int]:
        from cad_adapter.adapter_api_wrappers import create_rectangular_panel, move_point

        # Direction multiplier (top panel = 1, bottom panel = -1)
        direction_multiplier = 1 if self.is_top else -1

        # Calculate position
        moved_axis_p1 = move_point(slab_element.axis_start_point,
                                   slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + self.thickness) * .5 * direction_multiplier)
        moved_axis_p2 = move_point(slab_element.axis_end_point,
                                   slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + self.thickness) * .5 * direction_multiplier)
        moved_axis_p3 = move_point(slab_element.axis_height_point,
                                   slab_element.axis_local_thickness_direction,
                                   (config.beam_config.height + self.thickness) * .5 * direction_multiplier)

        panel_id = create_rectangular_panel(slab_element.slab_width,
                                            self.thickness, moved_axis_p1,
                                            moved_axis_p2,
                                            moved_axis_p3)

        self._element_ids = [panel_id]
        return [panel_id]