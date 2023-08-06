import os
from random import randint
import sys


class TicTacToe:
    def __init__(self):
        self.grid = [list("   ") for _ in range(3)]
        self.has_winner = False
        self.x_turn, self.o_turn = [None] * 2
        self.random()

    def play(self):
        self.clear()
        print("Tic Tac Toe\n")
        while not self.has_winner:
            self.show()

            turn = "X turn: " if self.x_turn else "O turn: "
            place = input(turn)

            row, col, player = self.transform(place)
            while (
                row >= len(self.grid)
                or col >= len(self.grid)
                or self.grid[row][col] != " "
            ):
                place = input(turn)
                row, col, player = self.transform(place)

            self.x_turn = not self.x_turn
            self.o_turn = not self.o_turn
            self.update(row, col, player)
            self.winner()

            self.clear()
            print("Tic Tac Toe\n")
            if self.full() and not self.has_winner:
                print("No winner.")
                break

        if self.has_winner:
            self.clear()
            self.show()
            print("Congrats, {}!".format(self.has_winner))

    def show(self):
        print("-------------")
        for row in self.grid:
            print("| {} |".format(" | ".join(row)))
            print("_____________")

    def update(self, row, col, player):
        self.grid[row][col] = player

    def transform(self, place):
        player = "X" if self.x_turn else "O"
        place = list(place)

        if len(place) < 2:
            row, col = len(self.grid), len(self.grid)
        else:
            place = [value for value in place if value != " "]
            row, col = int(place[0]), int(place[1])

        return row, col, player

    def winner(self):
        for row in self.grid:
            self.has_winner = (
                "X"
                if row[0] == row[1] == row[2] == "X"
                else "O"
                if row[0] == row[1] == row[2] == "O"
                else False
            )
            if self.has_winner:
                return

        for i in range(len(self.grid)):
            self.has_winner = (
                "X"
                if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] == "X"
                else "O"
                if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] == "O"
                else False
            )
            if self.has_winner:
                return

        self.has_winner = (
            "X"
            if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == "X"
            or self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == "X"
            else "O"
            if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == "O"
            or self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == "O"
            else False
        )

    def full(self):
        grid = [
            row
            for row in self.grid
            if row[0] != " " and row[1] != " " and row[2] != " "
        ]
        return len(grid) == len(self.grid)

    def clear(self):
        if sys.platform == "win32" and not self.has_winner:
            os.system("cls")
        elif not self.has_winner:
            os.system("clear")

    def reset(self):
        self.grid = [list("   ") for _ in range(3)]
        if self.has_winner:
            self.o_turn = True if self.has_winner == "O" else False
            self.x_turn = True if self.has_winner == "X" else False

        self.has_winner = False

    def random(self):
        rand = randint(0, 1)
        self.o_turn = True if rand else False
        self.x_turn = not self.o_turn
