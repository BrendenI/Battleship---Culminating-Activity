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

RULES: str = f"""{colored("Game Objective", "blue", attrs=["bold"])}

The object of Battleship is to try and sink all of the other player"s before they sink all of your ships. All of the other player"s ships are somewhere on his/her board.

You try and hit them by calling out the coordinates of one of the squares on the board. The other player also tries to hit your ships by calling out coordinates.

Neither you nor the other player can see the other"s board so you must try to guess where they are. Each board in the physical game has two grids: the lower (horizontal) section for the player"s ships and the upper part (vertical during play) for recording the player"s guesses.

----------

{colored("Starting A New Game", "blue", attrs=["bold"])}

Each player places the 5 ships somewhere on their board. The ships can only be placed vertically or horizontally. Diagonal placement is not allowed. No part of a ship may hang off the edge of the board. Ships may not overlap each other. No ships may be placed on another ship.

Once the guessing begins, the players may not move the ships.

The 5 ships are: Carrier (occupies 5 spaces), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2).

----------

{colored("Playing The Game", "blue", attrs=["bold"])}

Player"s take turns guessing by calling out the coordinates. The computer will tell you if you hit or missed. Both players" boards will be marked based on: red for hit, white for miss. For example, if you call out F6 and your opponent does not have any ship located at F6, your opponent"s board would be marked with a white marker. Your opponent records the miss by placing.

When all of the squares that one your ships occupies have been hit, the ship will be sunk.   You should announce "hit and sunk".  In the physical game, a red peg is placed on the top edge of the vertical board to indicate a sunk ship. 

As soon as all of one player"s ships have been sunk, the game ends.
"""


# Clear screen function.
def cls() -> None:
    os.system("clear")


cls()


def introSequence() -> None:
    """
    Prints a sequence of ASCII art and characters which make up the splash screen when initializing Battleship.
    """

    for index, image in enumerate(introGraphics.SHIP):
        print(image)

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

    while True:
        cls()

        print(introGraphics.TITLE_SHIP_FREEZE_FRAME)

        cprint("\nWhat would you like to do? (Choose a Number)\n", attrs=["bold"])

        cprint(f"1. {playOption}", "green", attrs=["bold"])
        cprint("2. View The Rules", "yellow", attrs=["bold"])
        cprint("3. Exit", "red", attrs=["bold"])

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


def main() -> None:
    # introSequence()

    allStats: list = []

    totalGames: int = 0

    while True:
        menuChoice: int = 1  # menu(True if totalGames == 0 else False)

        if menuChoice == 1:
            totalGames += 1

            stats = battleship.main()

            allStats.append(stats)
        elif menuChoice == 2:
            print(RULES)

            input(colored("\nPress [ENTER] to continue.", "green", attrs=["bold"]))

            continue
        elif menuChoice == 3:
            if not allStats:
                exit("Goodbye! 👋")
            else:
                cls()
                break
        else:
            raise ValueError()

    for i in allStats:
        print(i)


if __name__ == "__main__":
    main()