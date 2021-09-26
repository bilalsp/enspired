from __future__ import annotations

from queue import Queue
from itertools import product

from typing import Tuple, List

from enspired.coord import Coord
from enspired.room import Room
from enspired import utils


class Apartment:
    """Represent old-format plan-matrix as a collection of `Room` objects."""

    def __init__(self, size: Tuple) -> None:
        """Create an appartment of specified size without rooms.
        
        Args:
            size: length and width of the apartment.
        """
        self.size = size
        self.info = {'W': 0, 'P': 0, 'S': 0, 'C': 0}
        self._rooms = []
        self._index = 0

    def __iter__(self) -> Apartment:
        return self

    def __next__(self) -> Room:
        if self._index >= len(self._rooms):
            raise StopIteration
        room = self._rooms[self._index]
        self._index += 1
        return room

    @staticmethod
    def from_plan_matrix(plan_matrix: List[List[str]]) -> Apartment:
        """Create an appartment with empty rooms (without any chair).
        
        Args:
            plan_matrix: Old-format plan as a 2D-matrix.
        
        Returns:
            The `Apartment` with empty rooms.
        """
        apartment_size = len(plan_matrix), len(plan_matrix[0])
        apartment = Apartment(size=apartment_size)

        # Queue for top left corners of the rooms with next boundary coordinate 
        # and traversal direction
        top_left_corners_Q = Queue()
        
        # List to store processed top left corners to avoid reptations
        processed_top_left_corners = []

        # First top left corner
        top_left_corner = utils.get_first_top_left_corner(plan_matrix)
        top_left_corners_Q = utils.feed_in_Q(top_left_corner, None, 
                                             plan_matrix, 
                                             top_left_corners_Q,
                                             processed_top_left_corners)

        while not top_left_corners_Q.empty():
            # find a closed loop in a `plan` matrix starting from 
            # top left corner of room
            top_left_cor, next_boundary_elem, direction = \
                top_left_corners_Q.get()
            processed_top_left_corners.append(
                (top_left_cor, next_boundary_elem, direction))

            closed_boundary = [top_left_cor, next_boundary_elem]
            prev_coord, cur_coord = top_left_cor, next_boundary_elem

            while top_left_cor != cur_coord:
                cur_point = plan_matrix[cur_coord.x][cur_coord.y]
                next_coord, direction = utils.next_move(cur_coord, prev_coord, 
                                                        direction, plan_matrix) 
            
                # if current point is a corner 
                if cur_point == '+':
                    top_left_corners_Q = utils.feed_in_Q(
                        cur_coord, next_coord, 
                        plan_matrix, 
                        top_left_corners_Q,
                        processed_top_left_corners)

                prev_coord = cur_coord
                cur_coord = next_coord

                closed_boundary.append(cur_coord)
            
            # Create a new room with closed boundary
            room = Room(closed_boundary)
            
            # add new room to the apartment
            apartment.__add_room(room)

        return apartment

    def furnish(self, plan_matrix: List[List[str]]) -> None:
        """Put the chairs in correct rooms.
        
        Args:
            plan_matrix: Old-format plan as a 2D-matrix.
        """
        length, width = self.size
        type_of_chairs = ['W', 'P', 'S', 'C']

        # traverse over each cell of `plan_matrix`
        for i, j in product(range(length), range(width)):
            is_chair = plan_matrix[i][j] in type_of_chairs
            if is_chair:
                chair_coord = Coord(i, j)
                # add chair to the correct room of apartment
                self.__add_chair_to_room(chair_coord, plan_matrix)
            
            # room name found
            if plan_matrix[i][j] == '(':
                name_start_coord = Coord(i, j)
                # add room name 
                self.__add_room_name(name_start_coord, plan_matrix)

    def sort(self) -> None:
        """Sort the appartment's rooms by `room_name`."""
        self._rooms.sort()

    def clean(self) -> None:
        """Remove duplicate rooms"""
        temp_rooms_id = set()
        temp_rooms = [] 

        for room in self._rooms:
            if room.id not in temp_rooms_id:
                temp_rooms.append(room)
                temp_rooms_id.add(room.id)
        self._rooms = temp_rooms

    ###########################################################
    #                 Private Methods
    ###########################################################
    
    def __add_room(self, room: Room) -> None:
        """Add room to the appartment."""
        self._rooms.append(room)

    def __add_chair_to_room(self, chair_coord: Coord, 
                            plan_matrix: List[List[str]]):
        """Add chair to the correct room"""
        chair = plan_matrix[chair_coord.x][chair_coord.y]

        # left and right boundary coords w.r.t chair_coord
        boundary_coords = utils.get_left_right_boundary_coords(
            chair_coord, plan_matrix)
       
        for room in self._rooms:
            if boundary_coords in room:
                room.add_chair(chair)  
            
        # increament the chair count of appartment
        self.info[chair] += 1

    def __add_room_name(self, name_start_coord: Coord, 
                        plan_matrix: List[List[str]]):
        """Assign room name"""
        room_name = utils.get_room_name(name_start_coord, plan_matrix)
        # left and right boundary coords w.r.t name_start_coord
        boundary_coords = utils.get_left_right_boundary_coords(
            name_start_coord, plan_matrix)
        
        for room in self._rooms:
            if boundary_coords in room:
                room.name = room_name 
                room.id = hash(str(name_start_coord))
