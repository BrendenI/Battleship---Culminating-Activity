import random
from copy import deepcopy as copy
from termcolor import colored

from classes.Ship import Ship
from classes.SunkShip import SunkShip
from classes.Coordinate import Coordinate
from classes.Player import Player

from functions import utils

class Board:
    def __init__(self, rows: list[list[Coordinate]]):
        self.rows = rows
        self.shipLocations = {}
        self.sunkShips = []
        self.tempBoard = None

    def getRows(self) -> list[list[Coordinate]]:
        """
        This function returns all of the rows.
        """
        return self.rows

    def getCellData(self, x: int, y: int) -> Coordinate:
        """
        This function returns the data for a specific cell. Use indices: -1 < x < 10.
        """
        if x > 9 or x < 0 or y > 9 or y < 0:
            raise ValueError("board.getCellData was provided an input that satisfies: x > 9 or x < 0 or y > 9 or y < 0")

        return self.rows[y][x]
            

    def tempAddShip(self, startCoordinates: list[int], endCoordinates: list[int], shipData) -> list[list[Coordinate]]:
        """
        This function temporarily adds a ship to the board. This is used during ship placement to avoid interfering with the actual board.
        """
        tempRows: list[list[Coordinate]] = copy(self.rows)

        if startCoordinates[0] == endCoordinates[0]:
            for row in range(
                endCoordinates[1]
                if endCoordinates[1] < startCoordinates[1]
                else startCoordinates[1],
                (
                    endCoordinates[1]
                    if endCoordinates[1] > startCoordinates[1]
                    else startCoordinates[1]
                )
                + 1,
            ):
                tempRows[row][startCoordinates[0]].setShip(shipData)
        elif startCoordinates[1] == endCoordinates[1]:
            for point in tempRows[startCoordinates[1]][
                startCoordinates[0]
                if startCoordinates[0] < endCoordinates[0]
                else endCoordinates[0] : startCoordinates[0] + 1
                if startCoordinates[0] > endCoordinates[0]
                else endCoordinates[0] + 1
            ]:
                point.setShip(shipData)
        else:
            raise Exception(
                "From utils.classes: Error generating ship. startCoordinates[0] != endCoordinates[0] AND startCoordinates[1] != endCoordinates[1]."
            )

        self.tempBoard = tempRows

    def tempRemShip(self, startCoordinates: list[int], endCoordinates: list[int], shipData) -> list[list[Coordinate]]:
        """
        This function removes temporarily added ships from the board. This is used during ship placement to avoid interfering with the actual board.
        """
        tempRows: list[list[Coordinate]] = copy(self.rows)

        if startCoordinates[0] == endCoordinates[0]:
            for row in range(
                endCoordinates[1]
                if endCoordinates[1] < startCoordinates[1]
                else startCoordinates[1],
                (
                    endCoordinates[1]
                    if endCoordinates[1] > startCoordinates[1]
                    else startCoordinates[1]
                )
                + 1,
            ):
                tempRows[row][startCoordinates[0]].setShip(False)
        elif startCoordinates[1] == endCoordinates[1]:
            for point in tempRows[startCoordinates[1]][
                startCoordinates[0]
                if startCoordinates[0] < endCoordinates[0]
                else endCoordinates[0] : startCoordinates[0] + 1
                if startCoordinates[0] > endCoordinates[0]
                else endCoordinates[0] + 1
            ]:
                point.setShip(False)
        else:
            raise Exception(
                "From utils.classes: Error removing ship. startCoordinates[0] != endCoordinates[0] AND startCoordinates[1] != endCoordinates[1]."
            )

        self.tempBoard = tempRows

    def setShip(self, startCoordinates: list[int], endCoordinates: list[int], shipData: Ship) -> None:
        """
        This function sets a ship from start to end coordinates on the actual board. It also adds a start to end coordinate to the shipLocations dictionary.
        """
        if startCoordinates[0] == endCoordinates[0]:
            for row in range(
                endCoordinates[1]
                if endCoordinates[1] < startCoordinates[1]
                else startCoordinates[1],
                (
                    endCoordinates[1]
                    if endCoordinates[1] > startCoordinates[1]
                    else startCoordinates[1]
                )
                + 1,
            ):
                self.rows[row][startCoordinates[0]].setShip(shipData)
        elif startCoordinates[1] == endCoordinates[1]:
            for point in self.rows[startCoordinates[1]][
                startCoordinates[0]
                if startCoordinates[0] < endCoordinates[0]
                else endCoordinates[0] : startCoordinates[0] + 1
                if startCoordinates[0] > endCoordinates[0]
                else endCoordinates[0] + 1
            ]:
                point.setShip(shipData)
        else:
            raise Exception(
                "From utils.classes: Error generating ship. startCoordinates[0] != endCoordinates[0] AND startCoordinates[1] != endCoordinates[1]."
            )

        self.shipLocations[shipData.name] = dict(
            startCoordinates = startCoordinates,
            endCoordinates = endCoordinates
        )

    def collides(self, startCoordinates: list[int], endCoordinates: list[int]) -> bool:
        """
        This function checks if a coordinate range will collide with a ship. It returns a list of collisions if found.
        """
        coordsOfCurrent: list[list[int, int]] = utils.getCoordsFromStartToEnd(startCoordinates, endCoordinates)
        
        collisions: list[tuple[str, int]] = []
        
        for x, y in coordsOfCurrent:
            cellData = self.getCellData(x, y)

            if cellData.ship:
                collisions.append(cellData.coords())

        return collisions

    def getRandomRow(self) -> list[Coordinate]:
        """
        This function gets a random row from the board.
        """
        return random.choice(self.rows)

    def getRandomCoordinate(self, row: list[Coordinate], allowShips = False) -> Coordinate:
        """
        This function gets a random coordinate from a row. The function, by default, chooses a coordinate which doesn't have a ship, however this can be overwrote upon call.
        """
        randomCoordinates = row if allowShips else list(filter(lambda coordinate : coordinate.ship == False, row))

        if not randomCoordinates:
            return False

        return random.choice(randomCoordinates)