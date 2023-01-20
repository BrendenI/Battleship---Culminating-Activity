from classes.Ship import Ship
from classes.SunkShip import SunkShip

from functions import utils


class SmartShip:
    def __init__(self):
        self.origin = None
        self.current = None

    def rotation(self) -> str:
        """
        This function is used to determine the ship rotation using guessed coordinates. If the y-values are equal, the ship is horizontal, and vice-versa.
        """
        if not self.origin or not self.current:
            return None

        if self.current.rawCoords()[0] == self.origin.rawCoords()[0]:
            return "vertical"
        elif self.current.rawCoords()[1] == self.origin.rawCoords()[1]:
            return "horizontal"
        else:
            raise Exception(
                "Error determining smart ship rotation, classes.SmartShip.SmartShip."
            )
