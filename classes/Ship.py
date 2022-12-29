class Ship:
    """
    This class is used to store ship lengths & colours. It is not used for much...
    """
    def __init__(self, length: int, colour: str, name: str):
        self.length = length
        self.health = length
        self.colour = colour
        self.name = name
        self.shipHit = False