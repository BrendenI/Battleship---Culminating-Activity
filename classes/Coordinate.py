from classes.Ship import Ship

class Coordinate:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.colour = None
        self.name = None
        self.ship = False
        self.letterEquivalents = dict(
            A = 0,
            B = 1,
            C = 2,
            D = 3,
            E = 4,
            F = 5,
            G = 6,
            H = 7,
            I = 8,
            J = 9,
        )

    def convertToNumber(self, letter):
        if letter not in self.letterEquivalents:
            raise ValueError("Letter not in letterEquivalents. classes.Coordinate.convertToNumber")\

        return self.letterEquivalents[letter]
        
    def coords(self) -> tuple[str, int]:
        """
        This function returns the coordinates of the current point in human-readable form.
        """
        return self.column, self.row + 1

    def rawCoords(self) -> list[int]:
        """
        This function returns the coordinates of the current point in x, y form.
        """
        
        return [self.convertToNumber(self.column), self.row]
        
    def setShip(self, instance: Ship) -> bool:
        """
        This function sets the ship's prescence to the provided value.
        """
        self.ship = instance
        return self.ship