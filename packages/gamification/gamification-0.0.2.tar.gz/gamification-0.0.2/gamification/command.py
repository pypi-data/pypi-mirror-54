from gamification.game.tic_tac_toe import TicTacToe


def exec(game):

    if game in ["tic_tac_toe", "ttc", "Tic-Tac-Toe", "tic-tac-toe"]:
        tic_tac_toe = TicTacToe()
        tic_tac_toe.play()
        new_game = input("Do you want another game? [yN] ")
        while new_game.lower() in ["y", "yes"]:
            tic_tac_toe.reset()
            tic_tac_toe.play()
            new_game = input("Do you want another game? [yN] ")
