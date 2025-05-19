from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_id
from models.floor_structure import FloorStructure
from models.floor_structure_config import FloorStructureConfig


class FloorController:
    def __init__(self):
        pass

    def create_floor_structure(self, config: FloorStructureConfig):
        try:
            slab_element_id = self._filter_slab_element_id_from_elements()
            if slab_element_id is None:
                raise ValueError("No valid slab element found.")

            floor_structure = FloorStructure(slab_element_id, config)
            return floor_structure.generate_structure(config)

        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

    @staticmethod
    def _filter_slab_element_id_from_elements():
        elements = get_active_elements()
        slab_element_id = filter_slab_element_id(elements)
        return slab_element_id
