from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class BeamConfig:
    width: float = field(default=100)
    height: float = field(default=200)
    color: int = field(default=0)
    name: str = field(default="Beam")


@dataclass(frozen=True, slots=True)
class PanelConfig:
    thickness: float = field(default=18)
    color: int = field(default=0)
    name: str = field(default="Panel")

@dataclass(frozen=True, slots=True)
class FloorStructureConfig:
    spacing: float = field(default=0)
    beam_config: BeamConfig = field(default_factory=BeamConfig)
    top_panel_config: PanelConfig = field(default_factory=PanelConfig)
    bottom_panel_config: PanelConfig = field(default_factory=PanelConfig)
