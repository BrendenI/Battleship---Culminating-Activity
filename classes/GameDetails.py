from classes.Player import Player

class GameDetails:
    """
    This function stores all of the details for the game played. Most of the detail is stored in the Player class so this is a relatively small class.
    """
    def __init__(self, isPVP, winner: Player, players: list[Player]):
        self.isPVP = isPVP
        self.winner = winner
        self.players = players