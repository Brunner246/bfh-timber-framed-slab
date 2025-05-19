from dataclasses import dataclass, field
import cadwork

@dataclass(frozen=True, slots=True)
class BeamConfig:
    width: float = field(default=100)
    height: float = field(default=200)
    color: int = field(default=0)
    name: str = field(default="Beam")

@dataclass
class FloorStructureConfig:
    spacing: float = field(default=0)
    beam_config: BeamConfig = field(default_factory=BeamConfig)
