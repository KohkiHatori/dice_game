import os
from getpass import getpass
from colorama import Fore, Back, Style


class UI:

    @classmethod
    def show_round(cls, nth):
        if nth < 0:
            print(f"Tiebreaker{-nth}")
        else:
            print(f"Round{nth}")

    @classmethod
    def ask_to_roll(cls):
        a = input("Press any key to roll a die: ")

    @classmethod
    def whose_turn(cls, name):
        print(f"\n{name}'s turn: ")

    @classmethod
    def show_die(cls, player, point, nth):
        if nth == -1:
            print(f"{player.name} rolled {point}")
        elif nth == -2:
            print(f"{player.name} rolled {point} for extra")
        else:
            ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
            nth = ordinal(nth)
            print(f"{player.name}'s {nth} die: {point}")

    @classmethod
    def show_final_result(cls, winner):
        print(f"Winner is {winner.name} with {winner.total_score} points")

    @classmethod
    def show_podium(cls, scores):
        print("\nPodium")
        for index, items in enumerate(scores.items()):
            if index < 5:
                print(f"{index + 1}: {items[0]}: {items[1]} points")
            else:
                return 0

    @classmethod
    def login(cls, nth):
        print(f"Player{nth}")
        username = input("Username: ")
        password = getpass()
        return username, password

    @classmethod
    def show_state(cls, players, points):
        print("\n")
        for player, point in zip(players, points):
            print(f"{player.name}: Total: {player.total_score} This round: {point}")

    @classmethod
    def invalid(cls):
        print(Fore.RED + "username or password is invalid")
        print(Style.RESET_ALL)

    @classmethod
    def clear(cls):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    @classmethod
    def press_to_continue(cls):
        a = input("\nPress any key to continue: ")

    @classmethod
    def press_to_roll(cls):
        a = input("\nPress any key to roll: ")

    @classmethod
    def quit(cls):
        do_quit = input("Press [q] to quit or Enter to continue: ")
        if do_quit == "q":
            return True
        return False
