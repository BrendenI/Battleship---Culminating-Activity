from classes.Ship import Ship

from functions import utils


class Coordinate:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.colour = None
        self.name = None
        self.ship = False
        self.shipHit = False

    def coords(self) -> tuple[str, int]:
        """
        This function returns the coordinates of the current point in human-readable form.
        """
        return self.column, self.row + 1

    def rawCoords(self) -> list[int]:
        """
        This function returns the coordinates of the current point in x, y form.
        """

        return [utils.convertLetterToNumber(self.column), self.row]

    def setShip(self, instance: Ship) -> bool:
        """
        This function sets the ship's prescence to the provided value.
        """
        self.ship = instance
        return self.ship
