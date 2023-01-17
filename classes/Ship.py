class Ship:
    """
    This class is used to store ship data.
    """
    def __init__(self, length: int, colour: str, name: str):
        self.length = length
        self.colour = colour
        self.name = name
        self.health = length

    def isSunk(self) -> bool:
        """
        This functions returns whether or not the ship is sunk based on health.
        """
        return self.health < 1