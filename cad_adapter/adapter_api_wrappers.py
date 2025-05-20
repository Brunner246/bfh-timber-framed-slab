from typing import List

import cadwork


def filter_slab_element_ids(elements: List[int]) -> List[int]:
    # TODO: filter for framed floor elements
    pass


def move_point(point: cadwork.point_3d, direction_vector: cadwork.point_3d,
               distance: float) -> cadwork.point_3d:
    # TODO: Implement moving a point in 3D space: new_point = point + ... ...
    pass


def get_active_elements() -> List[int]:
    pass


def get_element_width(element_id: int) -> float:
    pass


def get_element_height(element_id: int) -> float:
    pass


def get_element_p1(element_id: int) -> cadwork.point_3d:
    # TODO: https://docs.cadwork.com/projects/cwapi3dpython/en/latest/examples/geometry/
    pass


def get_element_p2(element_id: int) -> cadwork.point_3d:
    # TODO: https://docs.cadwork.com/projects/cwapi3dpython/en/latest/examples/geometry/
    pass


def get_element_p3(element_id: int) -> cadwork.point_3d:
    # TODO: https://docs.cadwork.com/projects/cwapi3dpython/en/latest/examples/geometry/
    pass


def get_element_yl(element_id: int) -> cadwork.point_3d:
    # TODO: https://docs.cadwork.com/projects/cwapi3dpython/en/latest/examples/geometry/
    pass


def get_element_zl(element_id: int) -> cadwork.point_3d:
    # TODO: https://docs.cadwork.com/projects/cwapi3dpython/en/latest/examples/geometry/
    pass


def create_node(point: cadwork.point_3d) -> int:
    # TODO: create nodes to see start end point of beams
    condition: bool = True
    # TODO: ...
    pass


def create_rectangular_beam(start_point: cadwork.point_3d, end_point: cadwork.point_3d, width: float,
                            height: float,
                            height_axis_orientation: cadwork.point_3d
                            ) -> int:
    # TODO: implement creation of beam. p3 is e.g. start point + direction

    pass


def create_rectangular_panel(width: float, thickness: float, p1: cadwork.point_3d,
                             p2: cadwork.point_3d, p3: cadwork.point_3d) -> int:
    pass


def set_color(elements: List[int], color: int):
    pass


def set_name(elements: List[int], name: str):
    pass


def set_ifc_type(elements: List[int], ifc_entity_name: str):
    """Hook to overwrite the ifc type of an element"""

    import bim_controller as bc
    if len(elements) == 0:
        return
    ifc_type = bc.get_ifc2x3_element_type(elements[0])  # we need to get the type of a single element
    if ifc_entity_name == "IfcMember":
        ifc_type.set_ifc_member()
    # TODO: elif.. else

    # bc.set_ifc2x3_element_type(elements, ifc_type)


def set_subgroup(elements: List[int]):
    # TODO: implement subgroup attribute
    pass


def set_comment(elements: List[int], comment: str):
    # TODO: implement comment attribute
    pass


def set_endtype_start_pt(elements: List[int]):
    # TODO: implement endtype start point for each element
    pass
