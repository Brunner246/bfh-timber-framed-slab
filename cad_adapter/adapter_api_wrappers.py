from typing import List, Set

import attribute_controller as ac
import cadwork
import element_controller as ec
import geometry_controller as gc
import visualization_controller as vc


def filter_slab_element_ids(elements: List[int]) -> List[int]:
    # raise NotImplementedError()
    return list(filter(lambda x: ac.get_element_type(x).is_floor(), elements))


def move_point(point: cadwork.point_3d, direction_vector: cadwork.point_3d,
               distance: float) -> cadwork.point_3d:
    new_point = point + (direction_vector * distance)
    return new_point
    # raise NotImplementedError()


def get_active_elements() -> List[int]:
    return ec.get_active_identifiable_element_ids()
    # raise NotImplementedError()


def get_element_width(element_id: int) -> float:
    return gc.get_width(element_id)
    # raise NotImplementedError()


def get_element_height(element_id: int) -> float:
    return gc.get_height(element_id)
    # raise NotImplementedError()


def get_element_p1(element_id: int) -> cadwork.point_3d:
    return gc.get_p1(element_id)
    # raise NotImplementedError()


def get_element_p2(element_id: int) -> cadwork.point_3d:
    return gc.get_p2(element_id)
    # raise NotImplementedError()


def get_element_p3(element_id: int) -> cadwork.point_3d:
    return gc.get_p3(element_id)
    # raise NotImplementedError()


def get_element_yl(element_id: int) -> cadwork.point_3d:
    return gc.get_yl(element_id)
    # raise NotImplementedError()


def get_element_zl(element_id: int) -> cadwork.point_3d:
    return gc.get_zl(element_id)
    # raise NotImplementedError()


def create_node(point: cadwork.point_3d) -> int:
    return ec.create_node(point)
    # raise NotImplementedError()


def create_rectangular_beam(start_point: cadwork.point_3d, end_point: cadwork.point_3d, width: float,
                            height: float,
                            height_axis_orientation: cadwork.point_3d
                            ) -> int:
    # TODO: implement creation of beam. p3 is e.g. start point + direction

    return ec.create_rectangular_beam_points(width,
                                             height,
                                             start_point,
                                             end_point,
                                             start_point + height_axis_orientation)
    # raise NotImplementedError())


def create_rectangular_panel(width: float, thickness: float, p1: cadwork.point_3d,
                             p2: cadwork.point_3d, p3: cadwork.point_3d) -> int:
    return ec.create_rectangular_panel_points(width,
                                              thickness,
                                              p1,
                                              p2,
                                              p3)
    # raise NotImplementedError()


def set_color(elements: List[int], color: int):
    vc.set_color(elements, color)
    # raise NotImplementedError()


def set_name(elements: List[int], name: str):
    ac.set_name(elements, name)
    # raise NotImplementedError()


def set_ifc_type(elements: List[int], ifc_entity_name: str):
    """Hook to overwrite the ifc type of an element"""

    import bim_controller as bc
    if len(elements) == 0:
        return
    ifc_type = bc.get_ifc2x3_element_type(elements[0]) # we need to get the type of a single element
    if ifc_entity_name == "IfcMember":
        ifc_type.set_ifc_member()
    #TODO: elif.. else


    # bc.set_ifc2x3_element_type(elements, ifc_type)

    return

def set_subgroup(elements: List[int]):
    #TODO: implement subgroup attribute
    pass

def set_endtype_start_pt(elements: List[int]):
    import endtype_controller as etc
    etc.set_endtype_name_start(elements, "type")