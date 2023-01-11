import random
from copy import deepcopy as copy
from termcolor import colored

from classes.Ship import Ship
from classes.Player import Player


def getCoordsFromStartToEnd(startCoordinates: list[int, int], endCoordinates: list[int, int]) -> list[list[int, int]]:    
    if startCoordinates[1] == endCoordinates[1]:
        targetRange: list = range(startCoordinates[0] if startCoordinates[0] < endCoordinates[0] else endCoordinates[0], startCoordinates[0] + 1 if startCoordinates[0] > endCoordinates[0] else endCoordinates[0] + 1)

        return [[x, startCoordinates[1]] for x in targetRange]
    elif startCoordinates[0] == endCoordinates[0]:
        targetRange: list = range(startCoordinates[1] if startCoordinates[1] < endCoordinates[1] else endCoordinates[1], startCoordinates[1] + 1 if startCoordinates[1] > endCoordinates[1] else endCoordinates[1] + 1)

        return [[startCoordinates[0], y] for y in targetRange]
    else:
        raise Exception("Error checking if the ships collide. See utils.functions.getCoordsFromStartToEnd. startCoordinates[1] != endCoordinates[1] AND startCoordinates[0] != endCoordinates[0].")

def coordListToString(coordList: list[tuple[str, int]]) -> list[str]:
    newList: list[str] = []
    
    for coord in coordList:
        newList.append(f"{coord[0]}{coord[1]}")

    return newList

def convertLetterToNumber(letter: str) -> int:
    letterEquivalents = dict(
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
    
    if letter not in letterEquivalents:
        raise ValueError("Letter not in letterEquivalents. functions.utils.convertLetterToNumber")\

    return letterEquivalents[letter]

def convertNumberToLetter(number: str) -> str:
    numberEquivalents = {
        "0": "A",
        "1": "B",
        "2": "C",
        "3": "D",
        "4": "E",
        "5": "F",
        "6": "G",
        "7": "H",
        "8": "I",
        "9": "J",
    }
    
    if number not in numberEquivalents:
        raise ValueError("number not in numberEquivalents. functions.utils.convertNumberToLetter")\

    return numberEquivalents[number]