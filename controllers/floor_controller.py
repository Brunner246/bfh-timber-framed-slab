from cad_adapter.adapter_api_wrappers import get_active_elements, filter_slab_element_ids
from models.floor_structure import FloorStructure
from models.floor_structure_config import FloorStructureConfig


class FloorController:
    def __init__(self):
        pass

    def create_floor_structure(self, config: FloorStructureConfig):
        try:
            slab_element_ids = self._filter_slab_element_id_from_elements()
            if slab_element_ids is None:
                raise ValueError("No valid slab element found.")

            results = (FloorStructure(slab_id, config).generate_structure(config)
                       for slab_id in slab_element_ids)

            # Same is possible with a simple for loop for clarity
            # results = []
            # for slab_element_id in slab_element_ids:
            #     slab_structure = FloorStructure(slab_element_id, config)
            #     result = slab_structure.generate_structure(config)
            #     results.append(result)

            return all(results)

            # floor_structure = FloorStructure(slab_element_ids, config)
            # return floor_structure.generate_structure(config)

        except Exception as e:
            print(f"Error creating floor structure: {e}")
            return False

    @staticmethod
    def _filter_slab_element_id_from_elements() -> list[int]:
        elements = get_active_elements()
        slab_element_ids = filter_slab_element_ids(elements)
        return slab_element_ids
