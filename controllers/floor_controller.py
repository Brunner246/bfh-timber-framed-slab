from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_ids
from models.beam_component import BeamComponent
from models.floor_structure import FloorStructure
from models.floor_structure_config import FloorStructureConfig
from models.panel_component import TopPanelComponent, BottomPanelComponent


class FloorController:
    def __init__(self):
        pass

    def create_floor_structure(self, config: FloorStructureConfig):
        try:
            slab_element_ids = self._filter_slab_element_id_from_elements()
            if not slab_element_ids:
                raise ValueError("No valid slab element found.")

            results = []
            for slab_id in slab_element_ids:
                floor_structure = FloorStructure(slab_id, config)

                beam_component = BeamComponent(
                    name=config.beam_config.name,
                    color=config.beam_config.color,
                    width=config.beam_config.width,
                    height=config.beam_config.height
                )

                top_panel = TopPanelComponent(
                    name=config.top_panel_config.name,
                    color=config.top_panel_config.color
                )

                bottom_panel = BottomPanelComponent(
                    name=config.bottom_panel_config.name,
                    color=config.bottom_panel_config.color
                )

                floor_structure.add_component(beam_component)
                floor_structure.add_component(top_panel)
                floor_structure.add_component(bottom_panel)

                result = floor_structure.generate_structure(config)
                results.append(result)

            return all(results)
        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

    @staticmethod
    def _filter_slab_element_id_from_elements() -> list[int]:
        elements = get_active_elements()
        slab_element_ids = filter_slab_element_ids(elements)
        return slab_element_ids
