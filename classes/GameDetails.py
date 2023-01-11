from classes.Player import Player

class GameDetails:
    def __init__(self, isPVP, winner: Player, players: list[Player]):
        self.isPVP = isPVP
        self.winner = winner
        self.players = players