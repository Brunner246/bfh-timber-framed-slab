from typing import List

from cad_adapter.adapter_api_wrappers import set_subgroup
from .floor_structure_config import FloorStructureConfig
from .slab import setup_slab_data, Slab


class FloorStructure:
    def __init__(self, slab_element_id: int, config: FloorStructureConfig):
        self._slab_element_id = slab_element_id
        self._parent_slab_element = setup_slab_data(slab_element_id)
        self._config = config
        self._components = []
        self._created_element_ids = []

    @property
    def slab_element(self) -> Slab:
        return self._parent_slab_element

    def add_component(self, component):
        """Add a component to the floor structure"""
        self._components.append(component)
        return self

    def generate_structure(self, config: FloorStructureConfig) -> bool:
        try:
            for component in self._components:
                element_ids = component.create(self._parent_slab_element, config)
                component.apply_attributes()
                self._created_element_ids.extend(element_ids)

            if self._created_element_ids:
                self._set_sub_group(self._created_element_ids)

            return True
        except Exception as e:
            print(f"Error generating floor structure: {e}")
            return False

    def get_total_volume(self):
        # TODO: Calculate the total volume of the floor structure.
        volume = 0.0
        return volume

    @staticmethod
    def _set_sub_group(element_ids: List[int]):
        """Hook to set the subgroup of the elements."""
        set_subgroup(element_ids)