from classes.Ship import Ship

class SunkShip:
    """
    This class is used to store sunken ship data.
    """
    def __init__(self, ship: Ship, movesToSink: int):
        self.length = ship.length
        self.colour = ship.colour
        self.name = ship.name
        self.movesToSink = movesToSink