class Player:
    """
    This class is used to store player data.
    """
    def __init__(self, player: int, pvp: bool):
        self.player = player
        self.pvp = pvp
        self.hits = 0
        self.misses = 0
        self.totalShots = 0
        self.guessedCells = []

    def getRaw(self) -> int:
        """
        This function gets the raw player number.
        """
        return self.player

    def getHumanized(self) -> dict:
        """
        This function gets the player name, and returns it in the prefered tense.
        """
        if self.pvp:
            figure: dict = dict(
                singular="Player 1" if self.player == 1 else "Player 2",
                singular2="Player 1" if self.player == 1 else "Player 2",
                determiner="Player 1's" if self.player == 1 else "Player 2's",
                determiner2="Player 1's" if self.player == 1 else "Player 2's",
            )
            return figure
        else:
            figure: dict = dict(
                singular="Player" if self.player == 1 else "The Computer",
                singular2="You" if self.player == 1 else "The Computer",
                determiner="Your" if self.player == 1 else "The Computer's",
                determiner2="You're" if self.player == 1 else "The Computer is",
            )
            return figure

    def addGuessedCell(self, coordinates: list[int]) -> None:
        """
        This function adds the provided cell to the guesses array.
        """
        
        self.guessedCells.append(coordinates)
    
    def isGuessed(self, coordinates: list[int]) -> bool:
        """
        This function determines if the user has guessed the coordinate already.
        """
        
        return list(coordinates) in self.guessedCells