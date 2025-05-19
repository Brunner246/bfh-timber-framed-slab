from models.floor_structure_config import FloorStructureConfig


class FloorViewModel:
    def __init__(self, controller):
        self.controller = controller
        self.config: FloorStructureConfig | None = None

    def set_config(self, config: FloorStructureConfig):
        self.config = config

    def create_structure(self):
        if not self.config:
            raise ValueError("Configuration not set.")
        result = self.controller.create_floor_structure(self.config)
        return result
