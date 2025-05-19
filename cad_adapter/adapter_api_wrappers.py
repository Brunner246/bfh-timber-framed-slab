from typing import List

import attribute_controller as ac
import cadwork
import element_controller as ec
import geometry_controller as gc
import visualization_controller as vc

def filter_slab_element_id(elements: List[int]) -> int:
    # raise NotImplementedError()
    return next(filter(lambda x: ac.get_element_type(x).is_floor(), elements), None)


def move_point(point: cadwork.point_3d, slab_element_y_vec: cadwork.point_3d,
               distance: float) -> cadwork.point_3d:
    new_point = point + slab_element_y_vec * distance
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

    #TODO: implement creation of beam. p3 is e.g. start point + direction

    return ec.create_rectangular_beam_points(width,
                                             height,
                                             start_point,
                                             end_point,
                                             start_point + height_axis_orientation)
    # raise NotImplementedError())

def set_color(elements: List[int], color: int):
    vc.set_color(elements, color)
    # raise NotImplementedError()
