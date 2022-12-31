from termcolor import colored

from classes.Ship import Ship
from classes.SunkShip import SunkShip
from classes.Coordinate import Coordinate
from classes.Player import Player

from functions import utils

class GameDetails:
    def __init__(self, isPVP, winner: Player, players: list[Player]):
        self.isPVP = isPVP
        self.winner = winner
        self.players = players