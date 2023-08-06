"""
gamification

Usage:
  gamification new [game]
  gamification [game]

  gamification -h | --help
  gamification -v | --version

Options:
  new [game] starts a new game if name is given, or lists all existing games
  [game]     starts the game with given name, or lists all existing games

Other options:
  -h --help  shows possible commands.
  -v --version  shows current version of the package.
Help:
  For suggestions/problems and etc. visit the github reposityory https://github.com/monzita/gamification
"""
import sys

from docopt import docopt

from . import command


VERSION = "0.0.1"

GAMES = ["Tic Tac Toe: ttc | tic_tac_toe | tic-tac-toe | Tic-Tac-Toe"]


def main():
    global VERSION
    global GAMES

    args = sys.argv

    if "game" in args:
        args.remove("game")

    path = args[0]
    game = set(args) - {path, "new"}

    if len(game) > 1:
        print("Choose only one game!")
        return
    elif not len(game):
        print("\nAVAILABLE GAMES: /NAME: COMMAND(S)/")
        print("-" * 20)
        print("\n".join(GAMES))
        return

    game = list(game)[0]
    args.remove(game)

    options = docopt(__doc__, version=VERSION)

    command.exec(game)
