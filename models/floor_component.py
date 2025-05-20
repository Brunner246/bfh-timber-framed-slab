from abc import ABC, abstractmethod
from typing import List, Optional

import cadwork

from models.floor_structure_config import FloorStructureConfig
from models.slab import Slab


class FloorComponent(ABC):
    def __init__(self, name: str, color: int):
        self._name: str = name
        self._color: int = color
        self._element_ids: List[int] = []
        self._ifc_type: Optional[str] = None

    @abstractmethod
    def create(self, slab_element: Slab, config: FloorStructureConfig) -> List[int]:
        """Create the component and return element IDs"""
        pass

    def apply_attributes(self):
        """Apply attributes to created elements"""
        if not self._element_ids:
            return

        from cad_adapter.adapter_api_wrappers import set_color, set_name, set_ifc_type
        set_color(self._element_ids, self._color)
        set_name(self._element_ids, self._name)

        if self._ifc_type:
            set_ifc_type(self._element_ids, self._ifc_type)

        self.apply_component_feature()


    def apply_component_feature(self):
        """Hook... """
        pass