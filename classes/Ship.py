class Ship:
    """
    This class is used to store ship lengths & colours. It is not used for much...
    """
    def __init__(self, length: int, colour: str, name: str):
        self.length = length
        self.colour = colour
        self.name = name
        self.health = length

    def isSunk(self) -> bool:
        return not bool(self.health)