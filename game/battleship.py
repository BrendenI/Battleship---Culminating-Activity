# Import all needed modules and packages.
import time
import os
import random
from termcolor import cprint, colored
from copy import deepcopy

# Import the local classes module.
from classes.Board import Board
from classes.Ship import Ship
from classes.SunkShip import SunkShip
from classes.Coordinate import Coordinate
from classes.GameDetails import GameDetails
from classes.Player import Player

from functions import utils

# Create a string of the first 10 letters of the alphabet.
ALPHAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:10]

# Create a dictionary of Ship objects with their traditional lengths.
SHIPS = dict(
    # carrier = Ship(5, "blue", "Carrier"),
    # battleship = Ship(4, "cyan", "Battleship"),
    # cruiser = Ship(3, "yellow", "Cruiser"),
    submarine = Ship(3, "magenta", "Submarine"),
    destroyer = Ship(2, "green", "Destroyer"),
)

SLEEP = 1

DEBUG = True

# Clear screen function.
def cls() -> None:
    os.system("clear")


# Define a function to print the game board.

def getFormattedRows(player: Player, opponent: Player, facingOpponent: bool, temp: bool, isOutcomeScreen: bool) -> list[list[str]]:
    """
    This function displays the board in it's current state. The board can also be hidden meaning the other player won't see the ship locations when displaying.
    """
    formattedRows: list[list[str]] = [f"​​​{ALPHAS}", ""]

    iterable: list[list[Coordinate]] = None

    if facingOpponent:
        if temp:
            iterable = opponent.board.tempBoard
        else:
            if isOutcomeScreen:
                iterable = player.board.rows
            else:
                iterable = opponent.board.rows
    else:
        if temp:
            iterable = player.board.tempBoard
        else:
            iterable = player.board.rows

    for num, row in enumerate(iterable, start=1):
        formattedRow: list[str] = []
        
        for coordinate in row:
            rawcoords = coordinate.rawCoords()
            
            if iterable[rawcoords[1]][rawcoords[0]].shipHit:
                formattedRow.append(colored("⛝", 'red'))
            elif opponent.isGuessed(coordinate.rawCoords()) or coordinate.ship:
                formattedRow.append("■") if opponent.isGuessed(coordinate.rawCoords()) else formattedRow.append(colored("■", coordinate.ship.colour)) if not facingOpponent else formattedRow.append("□")
            else:
                formattedRow.append("□")
            
        formattedRow.insert(0, f"{num}  " if num < 10 else f"{num} ")

        formattedRows.append(formattedRow)

    return formattedRows

def printBoard(player: Player, opponent: Player, hidden: bool, temp = False, isOutcomeScreen = False):
    # Iterate through the rows of the board.
    for row in getFormattedRows(player, opponent, hidden, temp, isOutcomeScreen):
        # Print each element in the row.
        print(*row, flush = True)


# Define a function to ask the user if they want to play against another player or the computer.
def versusPlayer() -> bool:
    """
    This function asks the user for their preferred play style (1 v. Comp & 1 v 1).

    Returns:
    bool: True if the user is not playing against the computer.
    """

    # Keep asking for input until a valid choice is made.
    while True:
        # Clear the screen.
        cls()

        # Print the options for play style.
        cprint("Choose a play style.\n", "blue", attrs=["bold"])
        cprint("1. Player v. Computer", attrs=["bold"])
        cprint("2. Player v. Player\n", attrs=["bold"])

        # Try to get the user's choice.
        try:
            styleChoice: int = int(input("> "))

            # If the choice is invalid, raise an exception.
            if styleChoice < 1 or styleChoice > 2:
                raise ValueError()

            # Clear the screen.
            cls()

            # Return True if the user wants to play against another player, False if they want to play against the computer.
            return False if styleChoice == 1 else True
        except:
            # If an exception is raised, print an error message and ask the user to try again.
            input(
                colored(
                    "\nError! Invalid input. Pick one of the numbers.\n\nPress [ENTER] to continue.",
                    "red",
                    attrs=["bold"],
                )
            )


# Define a function to generate the initial game board.
def generateNewBoard() -> list[list[Coordinate]]:
    """
    This function generates the blank boards for the start of the game.

    Returns:
    list[list[Coordinate]]: This function returns 10 nested lists. They all contain the rows of the board which are filled with coordinate classes."""

    # Create an empty list to store the rows of the board.
    rows: list[list[Coordinate]] = []

    # Iterate through the columns of the board.
    for column in range(10):
        # Assign a alpha and a number to the specific coordinate.
        row: list[Coordinate] = [
            Coordinate(alpha, column) for alpha in ALPHAS
        ]

        # Append the row to the rows list.
        rows.append(row)

    return rows


def getShipChoice() -> str:
    """
    This function asks the user for their preferred ship movement.

    Returns:
    str: The user's direction choice.
    """
    # Pause for 0.3 seconds. This is here because Replit is very slow.
    time.sleep(0.3)
    # Get the user's input and convert it to uppercase.
    choice: str = input(colored("\n> ", attrs=["bold"])).upper()
    # Pause for 0.3 seconds. This is here because Replit is very slow.
    time.sleep(0.3)

    # If the user's input is not a valid choice, raise an exception.
    if (
        choice != "W"
        and choice != "A"
        and choice != "S"
        and choice != "D"
        and choice != "N"
        and choice != "R"
    ):
        raise ValueError()

    # Return the user's input.
    return choice


def findBestRotation(startPos: list[int], endPos: list[int], shipLen: int) -> tuple[list[int, int], list[int, int]]:
    """
    This function uses an algorithm to determine the best possible rotation when placing a ship. This is the function that deals with the "R" input.

    Params:
    startPos: The current start position of the ship.
    endPos: The current start position of the ship.
    shipLen: The length of the current ship.

    Returns:
    tuple[list[int, int], list[int, int]]: This returns the new coordinates of the rotated ship.
    """
    # Calculate the amount of spaces the ship needs to move in order to rotate.
    amnt = shipLen - 1

    # Calculate the possible new end positions for the ship if it were to rotate up.
    up = endPos[1] - amnt
    # Calculate the possible new end positions for the ship if it were to rotate down.
    down = endPos[1] + amnt
    # Calculate the possible new end positions for the ship if it were to rotate left.
    left = endPos[0] - amnt
    # Calculate the possible new end positions for the ship if it were to rotate right.
    right = endPos[0] + amnt

    # If the ship can rotate up, return the new start and end positions.
    if up >= 0 and startPos[0] != endPos[0]:
        return startPos, [startPos[0], endPos[1] - amnt]
    # If the ship can rotate down, return the new start and end positions.
    elif down < 10 and startPos[0] != endPos[0]:
        return startPos, [startPos[0], endPos[1] + amnt]
    # If the ship can rotate left, return the new start and end positions.
    elif left >= 0 and startPos[1] != endPos[1]:
        return startPos, [endPos[0] - amnt, startPos[1]]
    # If the ship can rotate right, return the new start and end positions.
    elif right < 10 and startPos[1] != endPos[1]:
        return startPos, [endPos[0] + amnt, startPos[1]]
    # If the ship cannot rotate in any direction, raise an exception.
    else:
        raise Exception("Illegal Rotation Error. Dock 50 marks sir....")


def placeShip(player: Player, opponent: Player, data: Ship) -> None:
    """
    This function asks the user for their prefered movement, then executes it if possible.
    """

    humanized = player.getHumanized()

    # Calculate the index of the last element in the ship's starting row.
    endX: int = data.length - 1

    # Add the ship to the board using temporary coordinates.
    player.board.tempAddShip([0, 0], [endX, 0], data)

    # Set the current start and end coordinates for the ship to the temporary coordinates.
    currentStartCoord = [0, 0]
    currentEndCoord = [endX, 0]

    # Run the placement loop until the user places the ship.
    while True:
        # Clear the screen.
        cls()
        # Print instructions for placing the ship.
        cprint(
            f"{colored(humanized['singular'], 'magenta')}, place your {colored(data.name, 'blue', attrs=['bold'])} using the WASD keys. This ship takes up {data.length} spaces.\n\n{colored('Hint:', 'yellow', attrs=['bold'])} Type N to advance onto the next ship, or R to rotate the current ship.\n\n",
            attrs=["bold"],
        )
        # Print the board with the temporary ship placed.
        printBoard(player, opponent, False, True)

        # Initialize the user's choice as an empty string.
        choice: str = ""

        # Try to get the user's choice.
        try:
            choice: str = getShipChoice()
        # If there is an issue with the input, print an error message and continue the loop.
        except:
            input(
                colored(
                    "\nThere was an issue with that input! Use the WASD keys to move the ship.\n\nPress [ENTER] to continue.",
                    "red",
                    attrs=["bold"],
                )
            )

            continue

        # If the user wants to move the ship up,
        if choice == "W":
            # If the ship cannot move up because it is already at the top, show an error.
            if currentStartCoord[1] - 1 < 0 or currentEndCoord[1] - 1 < 0:
                input(
                    colored(
                        "\nYou cannot go up because you are already at the highest level!\n\nPress [ENTER] to continue.",
                        "red",
                        attrs=["bold"],
                    )
                )
                cls()

                continue

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

            # Replace the old coordinates.
            currentStartCoord = [currentStartCoord[0], currentStartCoord[1] - 1]
            currentEndCoord = [currentEndCoord[0], currentEndCoord[1] - 1]

            # Add the new ship.
            player.board.tempAddShip(currentStartCoord, currentEndCoord, data)
        elif choice == "A":
            # If the ship cannot move left because it is already at the furthest left, show an error.
            if currentStartCoord[0] - 1 < 0 or currentEndCoord[0] - 1 < 0:
                input(
                    colored(
                        "\nYou cannot go left because you are already at the left-most column!\n\nPress [ENTER] to continue.",
                        "red",
                        attrs=["bold"],
                    )
                )
                cls()

                continue

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

            # Replace the old coordinates.
            currentStartCoord = [currentStartCoord[0] - 1, currentStartCoord[1]]
            currentEndCoord = [currentEndCoord[0] - 1, currentEndCoord[1]]

            # Add the new ship.
            player.board.tempAddShip(currentStartCoord, currentEndCoord, data)
        elif choice == "S":
            # If the ship cannot move down because it is already at the bottom, show an error.
            if (currentStartCoord[1] + 1) > (10 - 1) or (currentEndCoord[1] + 1) > (
                10 - 1
            ):
                input(
                    colored(
                        "\nYou cannot go down because you are already at the lowest level!\n\nPress [ENTER] to continue.",
                        "red",
                        attrs=["bold"],
                    )
                )
                cls()

                continue

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

            # Replace the old coordinates.
            currentStartCoord = [currentStartCoord[0], currentStartCoord[1] + 1]
            currentEndCoord = [currentEndCoord[0], currentEndCoord[1] + 1]

            # Add the new ship.
            player.board.tempAddShip(currentStartCoord, currentEndCoord, data)
        elif choice == "D":
            # If the ship cannot move right because it is already at the furthest right, show an error.
            if (currentStartCoord[0] + 1) > 9 or (currentEndCoord[0] + 1) > 9:
                input(
                    colored(
                        "\nYou cannot go right because you are already at the right-most column!\n\nPress [ENTER] to continue.",
                        "red",
                        attrs=["bold"],
                    )
                )
                cls()

                continue

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

            # Replace the old coordinates.
            currentStartCoord = [currentStartCoord[0] + 1, currentStartCoord[1]]
            currentEndCoord = [currentEndCoord[0] + 1, currentEndCoord[1]]

            # Add the new ship.
            player.board.tempAddShip(currentStartCoord, currentEndCoord, data)
        elif choice == "R":
            # If the user chooses to rotate the ship;

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

            # Find the best rotation using the rotation algorithm & set the old coordinates to the new ones.
            currentStartCoord, currentEndCoord = findBestRotation(
                currentStartCoord, currentEndCoord, data.length
            )

            # Add the new ship.
            player.board.tempAddShip(currentStartCoord, currentEndCoord, data)
        else:
            # If the user chooses to place the next ship;

            # Check if the current position of the ship would collide with another.
            collisions: list[tuple[str, int]] = player.board.collides(
                currentStartCoord, currentEndCoord
            )

            # If there are collisions, print them out individually and prompt the user to move the ship.
            if collisions:
                input(
                    colored(
                        f"\nYou cannot overlap ships! The following ({len(collisions)}) coordinates overlap:\n\n{', '.join([f'({x}, {y})' for x, y in collisions])}\n\nPress [ENTER] to continue.",
                        "red",
                        attrs=["bold"],
                    )
                )
                cls()

                continue

            # If there are no collisions, set the ship to the specified location.
            player.board.setShip(currentStartCoord, currentEndCoord, deepcopy(data))

            return


def humanShipPlacement(player: Player, opponent: Player) -> None:
    """
    This function executes the main sequence of placing the ships. It will execute all of the ships from the dictionary.
    """

    # For each ship in the variable, place the ship using the above "placeShip" function.
    for ship, data in SHIPS.items():
        placeShip(player, opponent, data)


def computerShipPlacement(board: Board) -> None:
    """
    This function randomly generates ships onto the board for Player vs. Computer.

    Params:
    board: The computers board.
    """

    cprint(f"The computer is placing it's ships.\n", "blue", attrs=['bold'])
    
    def getBestDirection(
        point: Coordinate, shipLen: int
    ) -> list[list[int, int]]:
        # Get the raw coordinates of the point.
        coords = point.rawCoords()

        # Calculate the amount of spaces the ship needs to move in order to rotate.
        amnt = shipLen - 1

        # Calculate all of the end coordinates if the ship were to move in the corresponding direction.
        up = coords[1] - amnt
        down = coords[1] + amnt
        left = coords[0] - amnt
        right = coords[0] + amnt

        # Compile the checks into a dictionary. The checks will determine if the ship can move in the specified direction based on its position on the board.
        check = dict(
            up = up >= 0,
            down = down < 10,
            left = left >= 0,
            right = right < 10
        )

        # Compile the outcomes into a dictionary. The outcomes are the possible end and start coordinates if the ship were to move in the corresponing direction.
        outcomes = dict(
            up=[coords, [coords[0], up]],
            down=[coords, [coords[0], down]],
            left=[coords, [left, coords[1]]],
            right=[coords, [right, coords[1]]],
        )

        possibleDirections: list[str] = []

        # Iterate through all of the checks.
        for direction, possible in check.items():
            # Check if the movement would be valid.
            if possible:
                # Get the outcome of the move from the outcomes dictionary.
                start, end = outcomes[direction]

                # If the movement does not collide with any other ship, append the direction to the possible directions array.
                if not board.collides(start, end):
                    possibleDirections.append(direction)
                    # If the ship collides, find another location to place the ship.
                else:
                    return False

        # Pick a random direction from the possible directions.
        randomDirection: str = random.choice(possibleDirections)

        # Return the start and end coordinates of the random chosen direction.
        return outcomes[randomDirection]

    # Iterate through all of the ships & parse the data.
    for ship, data in SHIPS.items():
        while True:
            # Pick a random row from the board.
            randomRow = board.getRandomRow()

            # Pick a random coordinate from the random row.
            randomCoordinate = board.getRandomCoordinate(randomRow)

            # If there is no random coordinate which also does not have a ship, pick another random row.
            if not randomCoordinate:
                continue

            # Use the above algorithm to pick the best orientation for the ship.
            adjustedCoordinates: list[list[int, int]] = getBestDirection(
                randomCoordinate, data.length
            )

            # If there is no good rotation which also doesn't collide, pick another row and restart this process.
            if not adjustedCoordinates:
                continue

            # Parse the new rotated ship's coordinates.
            adjustedStartCoordinates, adjustedEndCoordinates = adjustedCoordinates

            # Set the AI's ship to the specified location from the algorithm.
            board.setShip(adjustedStartCoordinates, adjustedEndCoordinates, data)

            # Break the loop & continue this process for the next ship(s).
            break

    time.sleep(SLEEP * 0.60)
    cprint(f"The computer has placed it's ships!\n\n(Continuing in {SLEEP} seconds.)", "cyan", attrs=['bold'])


def invertPlayer(currentPlayer: Player, players: list[Player]) -> Player:
    """
    This function flips the current player.

    Params:
    currentPlayer: The current player.
    players: The array of players.
    """
    # Get the current player's raw number.                     
    if currentPlayer.getRaw() == 1:
        # If the current player is #1, return the player #2 instance.
        return players[1]
    else:
        # If the current player is #2, return the player #1 instance.
        return players[0]


def printStartingPlayer(player: Player) -> None:
    # Print the starting player.    
    cprint(f"{(player.getHumanized()['determiner2'])} starting first!\n\n(Continuing in {SLEEP} seconds.)", "green", attrs=['bold'])
    
    time.sleep(SLEEP)
    
    cls()


def displayStats(player: Player, opponent: Player) -> None:
    addresses = player.getHumanized()
    
    print(colored(f"{addresses['determiner']} Guesses:", "green", attrs=['bold']), ", ".join(utils.coordListToString([[utils.convertNumberToLetter(str(cell[0])), cell[1] + 1] for cell in player.guessedCells])) if player.guessedCells else "N/A", "\n")
    print(colored(f"{addresses['determiner']} Total Shots:", "cyan", attrs=['bold']), player.totalShots)
    print(colored(f"{addresses['determiner']} Hits:", "red", attrs=['bold']), player.hits)
    print(colored(f"{addresses['determiner']} Misses:", "yellow", attrs=['bold']), player.misses, "\n")
    print(colored(f"Ships {addresses['singular2']} Sunk:", "magenta", attrs=['bold']), len(opponent.board.sunkShips))
    print(colored(f"{addresses['determiner']} Ships That Have Been Sunk:", "magenta", attrs=['bold']), len(player.board.sunkShips), "\n\n")


def getHumanMove(player: Player, opponent: Player) -> list[int]:
    while True:
        cls()

        humanizedOpponent = opponent.getHumanized()
        humanizedPlayer = player.getHumanized()

        cprint(f"{humanizedPlayer['singular']}, pick a cell to attack! The format should be: 'X Y'; for example, 'A 5'.\n\n", "blue", attrs=['bold'])

        displayStats(player, opponent)

        cprint(f"{humanizedOpponent['determiner']} Board:\n", "blue", attrs=['bold'])
        
        printBoard(opponent, player, False if ((not player.pvp) and (opponent.getRaw() == 1)) or DEBUG else True, isOutcomeScreen = True)

        cprint(f"\n\n{humanizedPlayer['determiner']} Board:\n", "blue", attrs=['bold'])
        
        printBoard(player, opponent, False if ((not player.pvp) and (opponent.getRaw() == 1)) or DEBUG else True, isOutcomeScreen = True if player.pvp else False)

        choice: str = input("\n\n> ").upper().split()

        if len(choice) != 2 or not all([choice[0] in ALPHAS, choice[1].isdigit()]) or int(choice[1]) < 1 or int(choice[1]) > 10:
            input(
                colored(
                    "\nThat was not a valid coordinate! Follow the formatting listed above.\n\nPress [ENTER] to retry.",
                    "red",
                    attrs=["bold"]
                )
            )
            cls()

            continue

        choice = [utils.convertLetterToNumber(choice[0]), int(choice[1]) - 1]

        if player.isGuessed(choice):
            input(
                colored(
                    "\nYou already guessed that coordinate! Pick another.\n\nPress [ENTER] to retry.",
                    "red",
                    attrs=["bold"]
                )
            )
            cls()

            continue

        player.addGuessedCell(choice)
        
        return choice


def getComputerMove(player: Player, opponent: Player) -> list[int]:
    while True:
        randomRow = player.board.getRandomRow()

        # Pick a random coordinate from the random row.
        randomCoordinate: Coordinate = player.board.getRandomCoordinate(randomRow, True)

        # If the random coordinate has already been picked or there is none, pick another random coordinate.
        if not randomCoordinate or player.isGuessed(randomCoordinate.rawCoords()):
            continue
            
        player.addGuessedCell(randomCoordinate.rawCoords())

        return randomCoordinate.rawCoords()
        

def game() -> GameDetails:
    # Get the prefered game style. (PVP vs PVE)
    isPVP: bool = True# versusPlayer()

    # Create a new array for the players.
    players: list[Player] = [Player(1, isPVP), Player(2, isPVP)]

    # Generate the player's boards.
    for player in players:
        player.board: Board = Board(generateNewBoard())

    # Since player 1 is always human, place their ships.
    humanShipPlacement(players[0], players[1])
        
    # Clear the screen.
    cls()

    if isPVP:
        # If the game is PVP, place player 2's ships.
        humanShipPlacement(players[1], players[0])
    else:
        # If the game is PVE, randomly place the computer's ships.
        computerShipPlacement(players[1].board)
        time.sleep(SLEEP)

    # Clear the screen.
    cls()

    # Get a random starting player.
    player = random.choice(players)

    # Print who is starting.
    printStartingPlayer(player)

    # Initialize a loop for the main part of the game. (Picking ship launch coordinates and such...)
    while True:
        guess: list[int] = []

        opponent: Player = invertPlayer(player, players)
        
        humanized1: dict = players[0].getHumanized()
        humanized2: dict = players[1].getHumanized()
        
        humanizedPlayer: dict = humanized1 if player.getRaw() == 1 else humanized2
        humanizedOpponent: dict = humanized1 if player.getRaw() == 2 else humanized2
        
        if isPVP:
            guess = getHumanMove(player, opponent) if player.getRaw() == 1 else getHumanMove(player, opponent)

            cls()
        else:
            if player.getRaw() == 1:
                guess = getHumanMove(player, opponent)

                cls()
            else:
                cls()
                cprint("Generating computer guess...\n\n", "blue", attrs=["bold"])
                
                guess = getComputerMove(player, opponent)
                
                time.sleep(SLEEP * 0.60)
                
                cprint(f"Generated computer guess!\n\n(Continuing in {SLEEP} seconds.)", "cyan", attrs=["bold"])
                
                time.sleep(SLEEP * 0.60)

                cls()

        player.totalShots += 1
        
        guessCell: Coordinate = opponent.board.getCellData(guess[0], guess[1])

        if guessCell.ship:
            cprint(f"{humanizedPlayer['determiner']} Shot Hit {humanizedOpponent['determiner']} {guessCell.ship.name} On Cell: {''.join(map(str, guessCell.coords()))}!", "magenta", attrs=['bold', 'underline'])
            guessCell.shipHit = True
            guessCell.ship.health -= 1
            player.hits += 1
        else:
            cprint(f"{humanizedPlayer['determiner']} Shot Missed {humanizedOpponent['determiner']} Ship(s). {humanizedPlayer['singular2']} Guessed: {''.join(map(str, guessCell.coords()))}", attrs=['bold', 'underline'])
            player.misses += 1
        
        cprint(f"\n\n{humanized1['determiner']} Board:\n", "blue", attrs=['bold'])

        printBoard(players[0], players[1], True if (isPVP and not DEBUG) else False, isOutcomeScreen = True if isPVP else False)
        
        print("\n")

        cprint(f"{humanized2['determiner']} Board:\n", "blue", attrs=['bold'])

        printBoard(players[1], players[0], not DEBUG, isOutcomeScreen = True)

        if guessCell.ship and guessCell.ship.isSunk():
            cprint(f"\n\n{humanizedPlayer['singular2']} Sunk {humanizedOpponent['determiner']} {guessCell.ship.name}!", "red", attrs=['bold', 'underline'])
            
            sunkShip: SunkShip = SunkShip(guessCell.ship, player.totalShots)

            opponent.board.sunkShips.append(sunkShip)

        if len(opponent.board.sunkShips) == len(SHIPS):
            cls()
            
            cprint(f"{humanizedPlayer['singular2']} Won! {humanizedOpponent['determiner']} Ships Have All Been Sunk.", "cyan", attrs=['bold', 'underline'])
            
            input(colored("\n\nPress [ENTER] to continue.", "green", attrs=["bold"]))

            stats = GameDetails(isPVP, player, players)

            return stats

        input(colored("\n\nPress [ENTER] to continue.", "green", attrs=["bold"]))

        player = invertPlayer(player, players)
            


def main() -> GameDetails:
    """
    This function holds the main structure for the battleship game. Upon call, it will run the user through a game of Battleship.

    Returns:
    GameDetails: The class holds the stats for the specific game of Battleship.
    """
    gameStats: GameDetails = game()

    return gameStats