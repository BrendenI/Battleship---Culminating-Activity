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
from classes.SmartShip import SmartShip

from functions import utils

# Create a string of the first 10 letters of the alphabet.
ALPHAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:10]

# Create a dictionary of Ship objects with their traditional lengths.
SHIPS = dict(
    carrier = Ship(5, "blue", "Carrier"),
    battleship = Ship(4, "cyan", "Battleship"),
    cruiser = Ship(3, "yellow", "Cruiser"),
    submarine=Ship(3, "magenta", "Submarine"),
    destroyer=Ship(2, "green", "Destroyer"),
)

DEBUG = False

SLEEP = 0 if DEBUG else 4


# Clear screen function.
def cls() -> None:
    os.system("clear")


# Define a function to print the game board.


def getFormattedRows(
    player: Player,
    opponent: Player,
    facingOpponent: bool,
    temp: bool,
    isOutcomeScreen: bool,
) -> list[list[str]]:
    """
    This function displays the board in it's current state. The board can also be hidden meaning the other player won't see the ship locations when displaying.
    """
    formattedRows: list[list[str]] = [f"​​​{ALPHAS}", ""]

    iterable: list[list[Coordinate]] = None

    # If the board should be hidden;
    if facingOpponent:
        # If the board should be the temporary version;
        if temp:
            # Set the iterable to the opponent's temporary board.
            iterable = opponent.board.tempBoard
        # If the board should be the game version;
        else:
            # If the board should not be inverse;
            if isOutcomeScreen:
                # Set the iterable to the player's game board.
                iterable = player.board.rows
            # If the board should be inverse;
            else:
                # Set the iterable to the opponent's game board.
                iterable = opponent.board.rows
    # If the board should not be hidden;
    else:
        # If the board should be the temporary version;
        if temp:
            # Set the iterable to the player's temporary board.
            iterable = player.board.tempBoard
        # If the board should be the game version;
        else:
            # Set the iterable to the player's game board.
            iterable = player.board.rows

    # Iterate through the iterable and assign an index.
    for num, row in enumerate(iterable, start=1):
        formattedRow: list[str] = []

        for coordinate in row:
            # Get the raw coords of the specific point.
            rawcoords = coordinate.rawCoords()

            # If the ship was hit at the coord;
            if iterable[rawcoords[1]][rawcoords[0]].shipHit:
                # Append a red "X".
                formattedRow.append(colored("⛝", "red"))
            # If the opponent guessed the coordinate, or there is a ship;
            elif opponent.isGuessed(coordinate.rawCoords()) or coordinate.ship:
                # Append a white square if the opponent guessed the coordinate, else append a coloured square, coloured to the specific ship colour. If the board is to be hidden, append a normal square.
                formattedRow.append("■") if opponent.isGuessed(
                    coordinate.rawCoords()
                ) else formattedRow.append(
                    colored("■", coordinate.ship.colour)
                ) if not facingOpponent else formattedRow.append(
                    "□"
                )
            else:
                # Append a normal square if there is no special features of the coordinate.
                formattedRow.append("□")

        # Insert the numbers which are displayed along the Y-Axis. Also append proper spacing.
        formattedRow.insert(0, f"{num}  " if num < 10 else f"{num} ")

        # Append the finalized row to the formatted row array.
        formattedRows.append(formattedRow)

    return formattedRows


def printBoard(
    player: Player, opponent: Player, hidden: bool, temp=False, isOutcomeScreen=False
):
    # Iterate through the rows of the board.
    for row in getFormattedRows(player, opponent, hidden, temp, isOutcomeScreen):
        # Print each element in the row.
        print(*row, flush=True)


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
    list[list[Coordinate]]: This function returns 10 nested lists. They all contain the rows of the board which are filled with coordinate classes.
    """

    # Create an empty list to store the rows of the board.
    rows: list[list[Coordinate]] = []

    # Iterate through the columns of the board.
    for column in range(10):
        # Assign a alpha and a number to the specific coordinate.
        row: list[Coordinate] = [Coordinate(alpha, column) for alpha in ALPHAS]

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


def findBestRotation(
    startPos: list[int], endPos: list[int], shipLen: int
) -> tuple[list[int, int], list[int, int]]:
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
            f"{colored(humanized.get('singular'), 'magenta')}, place your {colored(data.name, 'blue', attrs=['bold'])} using the WASD keys. This ship takes up {data.length} spaces.\n\n{colored('Hint:', 'yellow', attrs=['bold'])} Type N to advance onto the next ship, or R to rotate the current ship.\n\n",
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

            # Find the best rotation using the rotation algorithm & set the old coordinates to the new ones.
            try:
                currentStartCoord, currentEndCoord = findBestRotation(
                    currentStartCoord, currentEndCoord, data.length
                )
            except:
                currentStartCoord, currentEndCoord = currentStartCoord, currentEndCoord
                input(
                    colored(
                        "\nThere was an error finding a suitable rotation for the ship! Move the ship elsewhere and try again.\n\nPress [ENTER] to try again.",
                        "red",
                        attrs=["bold"],
                    )
                )
                continue

            # Remove the old ship.
            player.board.tempRemShip(currentStartCoord, currentEndCoord, data)

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

    cprint(f"The computer is placing it's ships.\n", "blue", attrs=["bold"])

    def getBestDirection(point: Coordinate, shipLen: int) -> list[list[int, int]]:
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
        check = dict(up=up >= 0, down=down < 10, left=left >= 0, right=right < 10)

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

        if not possibleDirections:
            raise Exception("No suitable computer rotation.")

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

            try:
                # Use the above algorithm to pick the best orientation for the ship.
                adjustedCoordinates: list[list[int, int]] = getBestDirection(
                    randomCoordinate, data.length
                )
            except:
                continue

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
    cprint(
        f"The computer has placed it's ships!\n\n(Continuing in {SLEEP} seconds.)",
        "cyan",
        attrs=["bold"],
    )


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
    cprint(
        f"{(player.getHumanized().get('determiner2'))} starting first!\n\n(Continuing in {SLEEP} seconds.)",
        "green",
        attrs=["bold"],
    )

    time.sleep(SLEEP)

    cls()


def displayStats(player: Player, opponent: Player) -> None:
    # Get the humanized versions of the player names.
    addresses = player.getHumanized()

    # Display all of the current game stats.
    print(
        colored(f"{addresses.get('determiner')} Guesses:", "green", attrs=["bold"]),
        ", ".join(
            utils.coordListToString(
                [
                    [utils.convertNumberToLetter(str(cell[0])), cell[1] + 1]
                    for cell in player.guessedCells
                ]
            )
        )
        if player.guessedCells
        else "N/A",
        "\n",
    )
    print(
        colored(f"{addresses.get('determiner')} Total Shots:", "cyan", attrs=["bold"]),
        player.totalShots,
    )
    print(
        colored(f"{addresses.get('determiner')} Hits:", "red", attrs=["bold"]),
        player.hits,
    )
    print(
        colored(f"{addresses.get('determiner')} Misses:", "yellow", attrs=["bold"]),
        player.misses,
        "\n",
    )
    print(
        colored(f"Ships {addresses.get('singular2')} Sunk:", "magenta", attrs=["bold"]),
        len(opponent.board.sunkShips),
    )
    print(
        colored(
            f"{addresses.get('determiner')} Ships That Have Been Sunk:",
            "magenta",
            attrs=["bold"],
        ),
        len(player.board.sunkShips),
        "\n\n",
    )


def getHumanMove(player: Player, opponent: Player) -> list[int]:
    while True:
        cls()

        # Get the humanized versions of the player names.
        humanizedOpponent = opponent.getHumanized()
        humanizedPlayer = player.getHumanized()

        # Get the current player's move.
        cprint(
            f"{humanizedPlayer.get('singular')}, pick a cell to attack! The format should be: 'X Y'; for example, 'A 5'.\n\n",
            "blue",
            attrs=["bold"],
        )

        # Display the stats of the current player.
        displayStats(player, opponent)

        # Display the opponent's board.
        cprint(
            f"{humanizedOpponent.get('determiner')} Board:\n", "blue", attrs=["bold"]
        )

        printBoard(
            opponent,
            player,
            False if ((not player.pvp) and (opponent.getRaw() == 1)) or DEBUG else True,
            isOutcomeScreen=True,
        )

        # Display the player's board.
        cprint(
            f"\n\n{humanizedPlayer.get('determiner')} Board:\n", "blue", attrs=["bold"]
        )

        printBoard(
            player,
            opponent,
            False if ((not player.pvp) and (opponent.getRaw() == 2)) or DEBUG else True,
            isOutcomeScreen=True,
        )

        choice: str = input("\n\n> ").upper().split()

        # If the choice was incorrect, throw an error.
        if (
            len(choice) != 2
            or not all([choice[0] in ALPHAS, choice[1].isdigit()])
            or int(choice[1]) < 1
            or int(choice[1]) > 10
        ):
            input(
                colored(
                    "\nThat was not a valid coordinate! Follow the formatting listed above.\n\nPress [ENTER] to retry.",
                    "red",
                    attrs=["bold"],
                )
            )
            cls()

            continue

        # Convert the choice to an index array.
        choice = [utils.convertLetterToNumber(choice[0]), int(choice[1]) - 1]

        # If the player guessed the same coordinate, display an error.
        if player.isGuessed(choice):
            input(
                colored(
                    "\nYou already guessed that coordinate! Pick another.\n\nPress [ENTER] to retry.",
                    "red",
                    attrs=["bold"],
                )
            )
            cls()

            continue

        # Add the choice to the guessed cells and return the choice.
        player.addGuessedCell(choice)

        return choice


def getComputerMove(
    player: Player, opponent: Player, smartShip: SmartShip
) -> Coordinate:
    randomCoordinate: Coordinate = None

    while True:
        # If there is an original hit point;
        if smartShip.origin:
            # If there is a current hit point;
            if smartShip.current:
                # Determine the rotation of the ship using the 2 points.
                rotation: str = smartShip.rotation()

                # Get the current and origin's raw coordinates. (integer indicies)
                currentCoords: list[int] = smartShip.current.rawCoords()
                originCoords: list[int] = smartShip.origin.rawCoords()

                # If the ship is determined to be vertical;
                if rotation == "vertical":
                    # If the Y value of the current coordinate is less than the origin;
                    if currentCoords[1] < originCoords[1]:
                        # Check if the guess is possible;
                        if currentCoords[1] - 1 < 0:
                            # Reset the point if not.
                            smartShip.current = None

                            continue

                        # Get the coord class of the new coordinate. Subtract 1 from the Y coordinate. (Guess up)
                        coordClass: Coordinate = player.board.getCellData(
                            currentCoords[0], currentCoords[1] - 1
                        )

                        # Append the new coordinates to the guessed cells.
                        player.addGuessedCell(coordClass.rawCoords())

                        return coordClass
                    # If the Y value of the current coordinate is greater than the origin;
                    elif currentCoords[1] > originCoords[1]:
                        # Check if the guess is possible;
                        if currentCoords[1] + 1 > 9:
                            smartShip.current = None

                            continue

                        # Get the coord class of the new coordinate. Add 1 to the Y coordinate. (Guess down)
                        coordClass: Coordinate = player.board.getCellData(
                            currentCoords[0], currentCoords[1] + 1
                        )

                        # Append the new coordinates to the guessed cells.
                        player.addGuessedCell(coordClass.rawCoords())

                        return coordClass
                    else:
                        raise Exception(
                            "Illegal move. Couldn't smart guess up or down."
                        )
                # If the ship is determined to be horizontal;
                else:
                    # If the X value of the current coordinate is less than the origin;
                    if currentCoords[0] < originCoords[0]:
                        # Check if the guess is possible;
                        if currentCoords[0] - 1 < 0:
                            smartShip.current = None

                            continue

                        # Get the coord class of the new coordinate. Subtract 1 from the X coordinate. (Guess left)
                        coordClass: Coordinate = player.board.getCellData(
                            currentCoords[0] - 1, currentCoords[1]
                        )

                        # Append the new coordinates to the guessed cells.
                        player.addGuessedCell(coordClass.rawCoords())

                        return coordClass
                    # If the X value of the current coordinate is greater than the origin;
                    elif currentCoords[0] > originCoords[0]:
                        # Check if the guess is possible;
                        if currentCoords[0] + 1 > 9:
                            smartShip.current = None

                            continue

                        # Get the coord class of the new coordinate. Add 1 to the Y coordinate. (Guess down)
                        coordClass: Coordinate = player.board.getCellData(
                            currentCoords[0] + 1, currentCoords[1]
                        )

                        # Append the new coordinates to the guessed cells.
                        player.addGuessedCell(coordClass.rawCoords())

                        return coordClass
                    else:
                        raise Exception(
                            "Illegal move. Couldn't smart guess left or right."
                        )
            # If there is no current point; (Ship is hit for the first time)
            else:
                # Get the coords of the smart ship origin point.
                originCoords: list[int] = smartShip.origin.rawCoords()

                # Find results for the move if it were to move in the corresponding direction.
                up: list[int] = [originCoords[0], originCoords[1] - 1]
                down: list[int] = [originCoords[0], originCoords[1] + 1]
                left: list[int] = [originCoords[0] - 1, originCoords[1]]
                right: list[int] = [originCoords[0] + 1, originCoords[1]]

                # Pick a direction based on possibility, and if it is guessed or not.
                possibleDirections = list(
                    filter(
                        lambda coords: (coords[0] > -1 and coords[0] < 10)
                        and (coords[1] > -1 and coords[1] < 10)
                        and not player.isGuessed(coords),
                        [up, down, left, right],
                    )
                )

                # If there is no eligible directions, reset the points.
                if not possibleDirections:
                    smartShip.current = None
                    smartShip.origin = None

                    continue

                # Pick a random choice from a possible direction.
                randomCoordinate: list[int] = random.choice(possibleDirections)

                # Set the random coordinate to the class of the random choice from above.
                randomCoordinate: Coordinate = player.board.getCellData(
                    randomCoordinate[0], randomCoordinate[1]
                )
        # If there is no origin point.
        else:
            # Get a random row.
            randomRow = player.board.getRandomRow()

            # Pick a random coordinate from the random row.
            randomCoordinate = player.board.getRandomCoordinate(randomRow, True)

            # If the random coordinate has already been picked or there is none, pick another random coordinate.
            if not randomCoordinate or player.isGuessed(randomCoordinate.rawCoords()):
                continue

        # Add the target cell to the guessed cells.
        player.addGuessedCell(randomCoordinate.rawCoords())

        return randomCoordinate


def game() -> GameDetails:
    # Get the prefered game style. (PVP vs PVE)
    isPVP: bool = versusPlayer()

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

    # Init a var for the AI's smart feature. This feature activates when the AI hits a ship. THe AI will search around the hit location to try and sink the ship. This var contains the ship data.abs
    smartShip: SmartShip = SmartShip()

    # Initialize a loop for the main part of the game. (Picking ship launch coordinates and such...)
    while True:
        guess: list[int] = []

        # Find the opponent based on the current player.
        opponent: Player = invertPlayer(player, players)

        # Get the humanized variants of the players
        humanized1: dict = players[0].getHumanized()
        humanized2: dict = players[1].getHumanized()

        # Get the proper humanizations for the current player and opponent
        humanizedPlayer: dict = humanized1 if player.getRaw() == 1 else humanized2
        humanizedOpponent: dict = humanized1 if player.getRaw() == 2 else humanized2

        if isPVP:
            # Get the human move if it is PVP.
            guess = getHumanMove(player, opponent)

            cls()
        else:
            if player.getRaw() == 1:
                # Get the human move if it is player 1's turn.
                guess = getHumanMove(player, opponent)

                cls()
            else:
                cls()
                cprint("Generating computer guess...\n\n", "blue", attrs=["bold"])

                # Get the computers move.
                guess = getComputerMove(player, opponent, smartShip)

                time.sleep(SLEEP * 0.60)

                cprint(
                    f"Generated computer guess!\n\n(Continuing in {SLEEP} seconds.)",
                    "cyan",
                    attrs=["bold"],
                )

                time.sleep(SLEEP * 0.60)

                cls()

        # Add one to the total shots.
        player.totalShots += 1

        # If it is a PVE game and the player is 2, parse the coords into numbers.
        if not isPVP and player.getRaw() == 2:
            guess = guess.rawCoords()

        # Get the cell data of the guessed coord on the opponent's board.
        guessCell: Coordinate = opponent.board.getCellData(guess[0], guess[1])

        # If there is a ship at the guessed cell;
        if guessCell.ship:
            # Print the ship's hit message and edit the attributes of the ship to reflect.
            cprint(
                f"{humanizedPlayer.get('determiner')} Shot Hit {humanizedOpponent.get('determiner')} {guessCell.ship.name} On Cell: {''.join(map(str, guessCell.coords()))}!",
                "magenta",
                attrs=["bold", "underline"],
            )
            guessCell.shipHit = True
            guessCell.ship.health -= 1
            player.hits += 1

            # If the computer hit the ship;
            if player.getRaw() == 2 and not isPVP:
                # If there is an origin hit, set the current to the guessed cell.
                if smartShip.origin:
                    smartShip.current = guessCell
                # If there is no origin, set the origin to the hit.
                else:
                    smartShip.origin = guessCell
        # If the shot was a miss;
        else:
            # Print the miss and edit the player stats to reflect this.
            cprint(
                f"{humanizedPlayer.get('determiner')} Shot Missed {humanizedOpponent.get('determiner')} Ship(s). {humanizedPlayer.get('singular2')} Guessed: {''.join(map(str, guessCell.coords()))}",
                attrs=["bold", "underline"],
            )
            player.misses += 1

            # If the game is PVE and the player is 2;
            if player.getRaw() == 2 and not isPVP:
                # Reset the current position.
                if smartShip.origin:
                    smartShip.current = None

        # Display all of the boards.
        cprint(f"\n\n{humanized1.get('determiner')} Board:\n", "blue", attrs=["bold"])

        printBoard(
            players[0],
            players[1],
            True if (isPVP and not DEBUG) else False,
            isOutcomeScreen=True if isPVP else False,
        )

        print("\n")

        cprint(f"{humanized2.get('determiner')} Board:\n", "blue", attrs=["bold"])

        printBoard(players[1], players[0], not DEBUG, isOutcomeScreen=True)

        # If the ship is sunk;
        if guessCell.ship and guessCell.ship.isSunk():
            cprint(
                f"\n\n{humanizedPlayer.get('singular2')} Sunk {humanizedOpponent.get('determiner')} {guessCell.ship.name}!",
                "red",
                attrs=["bold", "underline"],
            )

            # Create a sunk ship class with all of the details.
            sunkShip: SunkShip = SunkShip(guessCell.ship, player.totalShots)

            # Add the sunk ship to the sunk ships array.
            opponent.board.sunkShips.append(sunkShip)

            # Set the ships origin and current to None.
            smartShip.current = None
            smartShip.origin = None

        # If all of the ships are sunk;
        if len(opponent.board.sunkShips) == len(SHIPS):
            cls()

            # Print the outcome and assemble the stats.
            cprint(
                f"{humanizedPlayer.get('singular2')} Won! {humanizedOpponent.get('determiner')} Ships Have All Been Sunk.",
                "cyan",
                attrs=["bold", "underline"],
            )

            input(colored("\n\nPress [ENTER] to continue.", "green", attrs=["bold"]))

            stats = GameDetails(isPVP, player, players)

            # Return the game's stats.
            return stats

        input(colored("\n\nPress [ENTER] to continue.", "green", attrs=["bold"]))

        # Invert the player if the game continues.
        player = invertPlayer(player, players)


def main() -> GameDetails:
    """
    This function holds the main structure for the battleship game. Upon call, it will run the user through a game of Battleship.

    Returns:
    GameDetails: The class holds the stats for the specific game of Battleship.
    """
    gameStats: GameDetails = game()

    return gameStats
