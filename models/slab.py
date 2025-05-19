from dataclasses import dataclass, field
import cadwork
import cad_adapter.adapter_api_wrappers as api_wrappers


@dataclass
class Slab:
    element_id: int
    axis_start_point: cadwork.point_3d
    axis_end_point: cadwork.point_3d
    axis_height_point: cadwork.point_3d
    slab_thickness: float
    slab_width: float
    axis_local_width_direction: cadwork.point_3d
    axis_local_thickness_direction: cadwork.point_3d
    axis_local_length_direction: cadwork.point_3d = field(init=False)

    def __post_init__(self):
        direction = cadwork.point_3d(
            self.axis_end_point.x - self.axis_start_point.x,
            self.axis_end_point.y - self.axis_start_point.y,
            self.axis_end_point.z - self.axis_start_point.z,
        )
        norm = (direction.x ** 2 + direction.y ** 2 + direction.z ** 2) ** 0.5
        self.axis_local_length_direction = cadwork.point_3d(
            direction.x / norm,
            direction.y / norm,
            direction.z / norm,
        )


def map_slab_data(slab_element_id: int) -> Slab:
    slab: Slab = Slab(
        element_id=slab_element_id,
        slab_width=api_wrappers.get_element_width(slab_element_id),
        slab_thickness=api_wrappers.get_element_height(slab_element_id),
        axis_end_point=api_wrappers.get_element_p2(slab_element_id),
        axis_start_point=api_wrappers.get_element_p1(slab_element_id),
        axis_height_point=api_wrappers.get_element_p3(slab_element_id),
        axis_local_thickness_direction=api_wrappers.get_element_zl(slab_element_id),
        axis_local_width_direction=api_wrappers.get_element_yl(slab_element_id)
    )

    return slab
