import cadwork

from models.geom_utils import normalize_vector


def calculate_direction_vectors(structure_1_start: cadwork.point_3d, structure_1_end: cadwork.point_3d,
                                structure_2_end: cadwork.point_3d):
    """Calculate normalized direction vectors for beam adjustment."""
    direction_vector_length = normalize_vector(structure_1_end, structure_1_start)
    direction_vector_width = normalize_vector(structure_2_end, structure_1_end)
    return direction_vector_length, direction_vector_width


def adjust_beam_points(structure_1_start: cadwork.point_3d, structure_1_end: cadwork.point_3d,
                       structure_2_start: cadwork.point_3d, structure_2_end: cadwork.point_3d,
                       direction_vector_length, direction_vector_width, beam_width: float):
    """Adjust beam points based on direction vectors and beam width."""
    structure_2_start = structure_2_start + direction_vector_length * beam_width * 0.5
    structure_2_end = structure_2_end - direction_vector_length * beam_width * 0.5
    structure_2_start = structure_2_start - direction_vector_width * beam_width * 0.5
    structure_2_end = structure_2_end - direction_vector_width * beam_width * 0.5

    structure_1_start = structure_1_start + direction_vector_length * beam_width * 0.5
    structure_1_end = structure_1_end - direction_vector_length * beam_width * 0.5
    structure_1_start = structure_1_start + direction_vector_width * beam_width * 0.5
    structure_1_end = structure_1_end + direction_vector_width * beam_width * 0.5

    return structure_1_start, structure_1_end, structure_2_start, structure_2_end


def calculate_primary_beam_points(structure_1_start: cadwork.point_3d, structure_1_end: cadwork.point_3d,
                                  structure_2_start: cadwork.point_3d, structure_2_end: cadwork.point_3d,
                                  beam_width: float):
    """Calculate primary beam points by first determining vectors and then adjusting points."""
    direction_vector_length, direction_vector_width = calculate_direction_vectors(
        structure_1_start, structure_1_end, structure_2_end)

    return adjust_beam_points(
        structure_1_start, structure_1_end, structure_2_start, structure_2_end,
        direction_vector_length, direction_vector_width, beam_width)