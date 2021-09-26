"""
The :mod:`enspired.utils` module includes helper utilities
"""
from typing import Tuple, List
from queue import Queue

from enspired.coord import Coord


def is_valid(plan_matrix: List[List[str]], coord: Coord) -> bool:
    """Check given coordinate valid.
    
    Args:
        plan_matrix: Old-format plan as a 2D-matrix.
        coord: coordinate of plan matrix.

    Return:
        It returns `True` if coordinate lies inside plan matrix, 
        otherwise `False`.
    """
    return 0 <= coord.x < len(plan_matrix) and \
        0 <= coord.y < len(plan_matrix[0])


def get_room_name(name_start_coord: Coord, plan_matrix: List[List[str]]) -> str:
    """Get room name.
    
    Args:
        name_start_coord: Coordinate of first letter of room name.
        plan_matrix: Old-format plan as a 2D-matrix.

    Returns:
        Room name.
    """
    name = []
    i, j = name_start_coord.x, name_start_coord.y
    while plan_matrix[i][j + 1] != ')':
        name.append(plan_matrix[i][j + 1])
        j += 1
    return "".join(name)


def next_move(cur_coord: Coord, prev_coord: Coord, direction: str, 
              plan_matrix: List[List[str]]) -> Tuple:
    """Move to the next coordinate in a plan matrix.
    
    Args:
        cur_coord: current coordinate.
        prev_coord: previous coordinate.
        direction: traversal direction.
        plan_matrix: Old-format plan as a 2D-matrix.

    Returns:
        next coordinate and new direction of traversal.
    """            
    cur_point = plan_matrix[cur_coord.x][cur_coord.y]

    # boundary_points with coordinate change
    boundary_points = {
        '-': {'right': Coord(0, 1), 'left': Coord(0, -1)}, 
        '|': {'up': Coord(-1, 0), 'down': Coord(1, 0)}, 
        '/': {'up': Coord(-1, 1), 'down': Coord(1, -1)},
        '\\': {'up': Coord(-1, -1), 'down': Coord(1, 1)}
    }

    # if current point is not a corner
    if cur_point != '+':
        coord_change = boundary_points[cur_point][direction]
        next_coord = cur_coord + coord_change
    else:
        # move anti-clockwise around the corner
        change_coords = [Coord(1, 1), Coord(0, 1), Coord(-1, 1), Coord(-1, 0), 
                         Coord(-1, -1), Coord(0, -1), Coord(1, -1), Coord(1, 0)]  
        direction_lst = ['up', 'left', 'down', 'down', 'down', 'right', 'up', 
                         'up']      
        
        change_coord = cur_coord - prev_coord
        start_index = change_coords.index(change_coord) + 1

        for _ in range(len(change_coords) - 1):
            change_coord = change_coords[start_index % len(change_coords)]  
            direction = direction_lst[start_index % len(direction_lst)] 

            next_coord = cur_coord - change_coord
            if is_valid(plan_matrix, next_coord):
                new_point = plan_matrix[next_coord.x][next_coord.y]
                if new_point in boundary_points.keys():
                    break
            start_index += 1   

    return next_coord, direction


def feed_in_Q(cur_coord: Coord, next_coord: Coord, plan_matrix: List[List[str]], 
              top_left_corners_Q: Queue, 
              processed_top_left_corners: List) -> Queue:
    """Find top left corners for other rooms and put in a `top_left_corners_Q`.

    Args: 
        cur_coord: current coordinate.
        next_coord: next coordinate.
        plan_matrix: Old-format plan as a 2D-matrix.
        top_left_corners_Q: top left corners queue
        processed_top_left_corners: list of processed top left corners

    Returns:
        `top_left_corners_Q` queue 
    """
    boundary_points = ['-', '|', '/', '\\']
    
    # check next boundary point clock-wise w.r.t. current coordinate
    change_coords = [(Coord(0, -1), 'right'), (Coord(-1, -1), 'down'), 
                     (Coord(-1, 0), 'down'), (Coord(-1, 1), 'down')]
    
    # list of new top corners
    lst_top_corners = []

    for change_coord, direction in change_coords:
        new_coord = cur_coord - change_coord

        if is_valid(plan_matrix, new_coord) and \
                plan_matrix[new_coord.x][new_coord.y] in boundary_points:
            lst_top_corners.append((new_coord, direction))

        if next_coord and (new_coord == next_coord):
            break  

    if len(lst_top_corners) < 2:
        return top_left_corners_Q

    for new_coord, direction in lst_top_corners[:-1]:
        if not (cur_coord, new_coord, direction) in processed_top_left_corners:
            top_left_corners_Q.put((cur_coord, new_coord, direction))  

    return top_left_corners_Q


def get_first_top_left_corner(plan_matrix: List[List[str]]):
    """Get top left corner of the appartment.

    Note: Consider the below situation of plan matrix, when top left corner 
          is not at `Coord(0,0)`. 
        +-----+
       /      |
      /       |

    Args: 
        plan_matrix: Old-format plan as a 2D-matrix.
    """
    i, j = 0, 0
    size_plan_matrix = len(plan_matrix), len(plan_matrix[0])
    while plan_matrix[i][j] != '+':
        if j == size_plan_matrix[1] - 1:
            i, j = i + 1, 0
        else:
            i += 1
    return Coord(i, j)


def get_left_right_boundary_coords(coord: Coord, plan_matrix: List[List[str]]):
    """Get left and right boundary coordinate of the room w.r.t. given coord.

    Args:
        coord: Coordinate of plan matrix.
        plan_matrix: Old-format plan as a 2D-matrix.
    """
    boundary_points = ['-', '|', '/', '\\']
    appartment_size = len(plan_matrix), len(plan_matrix[0])
    boundary_coords = []

    # left and right boundary coords w.r.t given coordinate
    for j in range(coord.y - 1, -1, -1):
        point = plan_matrix[coord.x][j]
        if point in boundary_points or point == '+':
            boundary_coords.append(Coord(coord.x, j))
            break

    for j in range(coord.y + 1, appartment_size[1]):
        point = plan_matrix[coord.x][j]
        if point in boundary_points or point == '+':
            boundary_coords.append(Coord(coord.x, j))
            break
        
    return boundary_coords
