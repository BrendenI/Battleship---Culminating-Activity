# Brenden Iannetta
# Mr. Brescacin - ICS3U
# December 16, 2022 -> January XX, 2023
# Culminating Activity
{
    # 0 - 85%:
    # Battleship is functional where the user can compete against the other player see two “screens” much like the real version of the game.
    # The game concludes when either player has sunk all 5 “battleships” of the other.
    #
    # 85 - 100%:
    # Battleship is functional where the user can compete against the computer or player
    # see two “screens” much like the real version of the game./
    #
    # The game concludes when either player has sunk all 5 “battleships” of the other
    # displays a win/loss message for the user.
    #
    # Better User Interaction – Do not allow the player to select the same cell twice. Modify the program to tell the user that they have already guessed that cell.
    #
    # Playability – Make your game user-friendly and playable. You need to decide what the interaction with the user will look like. Consider at the very least adding welcome and farewell messages.
    #
    # Error Proofing all input. Put the user in a safety bubble. They should not be able to input invalid input.
    #
    # Worth 30% of your grade and the due date is January 30, 2023.
}

# Import all needed modules and packages.
import time
import os
from termcolor import cprint, colored

from game import battleship
from assets import introGraphics
from functions import utils

from classes.GameDetails import GameDetails

RULES: str = f"""{colored("In-Game Symbols", "blue", attrs=["bold"])}

In Battleship, various symbols are used to denote grid cell meanings. In this version of Battleship, you will see the following symbols:


Non-Ship cells are shown with an outlined square: □

Ship cells are shown with a filled & coloured square: {colored("■", "blue")} {colored("■", "cyan")} {colored("■", "yellow")} {colored("■", "magenta")} {colored("■", "green")}

Missed shots are shown with a filled white square: ■

Hit cells are shown with a crossed out, red square: {colored("⛝", "red")}

----------

{colored("Game Objective", "blue", attrs=["bold"])}

The object of Battleship is to try and sink all of the other player's before they sink all of your ships. All of the other player's ships are somewhere on his/her board.

You try and hit them by calling out the coordinates of one of the squares on the board. The other player also tries to hit your ships by calling out coordinates.

Neither you nor the other player can see the other's board so you must try to guess where they are. Each board in the physical game has two grids: the lower (horizontal) section for the player's ships and the upper part (vertical during play) for recording the player's guesses.

----------

{colored("Starting A New Game", "blue", attrs=["bold"])}

Each player places the 5 ships somewhere on their board. The ships can only be placed vertically or horizontally. Diagonal placement is not allowed. No part of a ship may hang off the edge of the board. Ships may not overlap each other. No ships may be placed on another ship.

Once the guessing begins, the players may not move the ships.

The 5 ships are: Carrier (occupies 5 spaces), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2).

----------

{colored("Playing The Game", "blue", attrs=["bold"])}

Players take turns guessing by calling out the coordinates. The computer will tell you if you hit or missed. Both players' boards will be marked based on: red for hit, white for miss. For example, if you call out F6 and your opponent does not have any ship located at F6, your opponent's board would be marked with a white marker.

When all of the squares that one your ships occupies have been hit, the ship will be sunk.

As soon as all of one player"s ships have been sunk, the game ends & you have the option to play again or exit to stats.
"""


# Clear screen function.
def cls() -> None:
    os.system("clear")


cls()


def introSequence() -> None:
    """
    Prints a sequence of ASCII art and characters which make up the splash screen when initializing Battleship.
    """

    # For all of the rows in the intrp graphic, assign them an index.
    for index, image in enumerate(introGraphics.SHIP):
        print(image)

        # If the index is less than the amount of intro graphics, sleep for 0.35 seconds.
        if index < len(introGraphics.SHIP) - 1:
            time.sleep(0.35)

        cls()


def menu(firstGame: bool) -> int:
    """
    Asks the user for their choice of what they would like to do at the start of the program.

    Returns:
    int: Choice from the menu to be processed.
    """

    playOption: str = "Play Battleship" if firstGame else "Play Again"
    exitOption: str = "Exit" if firstGame else "Exit & View All Game Stats"

    while True:
        cls()

        # Print the freeze frame for loop ability (so you don't have to go thru the animation every invalid input).
        print(introGraphics.TITLE_SHIP_FREEZE_FRAME)

        # Print the options.
        cprint("\nWhat would you like to do? (Choose a Number)\n", attrs=["bold"])

        cprint(f"1. {playOption}", "green", attrs=["bold"])
        cprint("2. View The Rules", "yellow", attrs=["bold"])
        cprint(f"3. {exitOption}", "red", attrs=["bold"])

        # Try to get a valid input and return it. If it is invalid, retry the loop with an error.
        try:
            choice: int = int(input("\n> "))

            if choice < 1 or choice > 3:
                raise ValueError()

            cls()
            return choice
        except:
            input(
                colored(
                    "\nError! Please enter one of the numbers!\n\nPress [ENTER] to Continue",
                    "red",
                    attrs=["bold"],
                )
            )
            cls()
            continue


def printGameStats(gameNumber: int, gameStats: GameDetails):
    # Print the game number
    cprint(f"Game {gameNumber}:\n", "blue", attrs=["bold", "underline"])

    # Print the winner.
    print(
        colored("Winner:", "blue", attrs=["bold"]),
        colored(gameStats.winner.getHumanized()["singular2"], attrs=["bold"]),
        "\n",
    )

    # Loop through the player's stats.
    for player in gameStats.players:
        # Determine the opponent using the current player.
        opponent = (
            gameStats.players[0] if player.getRaw() == 2 else gameStats.players[1]
        )

        # Print the header for the stats.
        cprint(
            f"{player.getHumanized()['determiner']} Stats:\n",
            "grey",
            attrs=["bold", "underline"],
        )

        # Print the guesses of the player.
        print(
            colored(f"Guesses:", "green", attrs=["bold"]),
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
        )
        print()
        # Print the total guesses.
        print(colored("Total Guesses:", "cyan", attrs=["bold"]), player.totalShots)
        # Print the total hits.
        print(colored("Hits:", "red", attrs=["bold"]), player.hits)
        # Print the total misses.
        print(colored("Misses:", "yellow", attrs=["bold"]), player.misses)
        # Print the hit to miss ratio and then make sure that it is possible using a big if/else comprehension.
        print(
            colored("Hit To Miss Ratio:", "magenta", attrs=["bold"]),
            round(player.hits / player.misses, 2)
            if player.hits and player.misses
            else player.hits
            if not player.misses and player.hits
            else "(Insufficient Data)",
        )
        print()
        # Print the ships that the player sunk.
        cprint(
            f"Ships {player.getHumanized()['singular2']} Sunk:\n",
            "grey",
            attrs=["bold", "underline"],
        )

        # If there was no ships sunk, print so.
        if not opponent.board.sunkShips:
            cprint("(None)", "red", attrs=["bold"])
        else:
            # Loop through all of the ships that were sunk.
            for ship in opponent.board.sunkShips:
                # Print the player that sunk the ship, the player that got their ships sunk, the name of the ship that was sunk, and the amount of moves that it took for the ship to be sunk.
                cprint(
                    f"{player.getHumanized()['singular2']} Sunk {opponent.getHumanized()['determiner']} {ship.name} After {ship.movesToSink} Move{'s' if ship.movesToSink != 1 else ''}.",
                    "green",
                    attrs=["bold"],
                )

        # Print the player's board at it's end of game state.
        cprint(
            f"\n{player.getHumanized()['determiner']} Board:\n",
            "grey",
            attrs=["bold", "underline"],
        )

        battleship.printBoard(player, opponent, False)

        # Print the separator if it is the first player.
        if player.getRaw() == 1:
            print("\n\n~---------------~\n\n")


def main() -> None:
    # Print the intro graphics.
    introSequence()

    # Init lists for all of the stats and the total number of games played.
    allStats: list = []

    totalGames: int = 0

    while True:
        # Get the menu choice from the user.
        menuChoice: int = menu(True if totalGames == 0 else False)

        # If the user chooses 1, launch the game.
        if menuChoice == 1:
            totalGames += 1

            stats = battleship.main()

            allStats.append(stats)
        # If the user chooses 2, launch the rules.
        elif menuChoice == 2:
            print(RULES)

            input(colored("\nPress [ENTER] to continue.", "green", attrs=["bold"]))

            continue
        # If the user chooses 3, exit to stats if applicable.
        elif menuChoice == 3:
            if not allStats:
                exit("Goodbye! 👋")
            else:
                cls()
                break
        else:
            raise ValueError()

    # Loop through all of the stats and display them.
    for gameNumber, gameStat in enumerate(allStats, start=1):
        if gameNumber > 1:
            cprint(
                "\n\n~----------------------------------------~\n\n",
                "red",
                attrs=["bold"],
            )

        printGameStats(gameNumber, gameStat)


if __name__ == "__main__":
    main()
