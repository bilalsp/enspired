from typing import List


class Room:
    """Represent closed boundary in floor plan as a room."""

    def __init__(self, boundary: List) -> None:
        """"Create a room for an apartment.
        
        Args:
            boundary: coordinates of closed boundary
        """
        self.boundary = boundary
        self.info = {'W': 0, 'P': 0, 'S': 0, 'C': 0}
        self._id = None        
        self._name = None
        
    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, room_id: str) -> None:
        self._id = room_id

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, room_name: str) -> None:
        self._name = room_name

    def add_chair(self, chair: str):
        """Assign chair to the room.
        
        Args:
            chair: letter representing a chair.
        """
        self.info[chair] += 1

    def __lt__(self, other):
        return self.name < other.name

    def __contains__(self, boundary_coords):
        match_count = 0
        for boundary_coord in boundary_coords:    
            if boundary_coord in self.boundary:
                match_count += 1 
        return match_count == len(boundary_coords)
