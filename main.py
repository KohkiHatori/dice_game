import random
import json
import math
from ui import UI

DATA_FILE = "database.json"


class Game:

    def __init__(self, num_dice=2, num_round=5, num_player=2):
        self.num_dice = num_dice
        self.num_round = num_round
        self.num_player = num_player
        self._players = []
        self.__database = self.load_database()
        self.__users = self.__database["users"]
        self.scores = self.__database["scores"]

    def init_players(self):
        while len(self._players) < self.num_player:
            username, password = UI.login(len(self._players) + 1)
            if self.authenticate(username, password):
                self._players.append(Player(username))
            else:
                UI.invalid()
                if UI.quit():
                    return False
            UI.clear()
        return True

    def authenticate(self, username, password):
        if username in self.__users.keys():
            if password == self.__users[username]:
                return True
        return False

    def modify_database(self, winner):
        if winner.name in self.scores.keys():
            if winner.total_score > int(self.scores[winner.name]):
                self.scores.update({winner.name: winner.total_score})
        self.sort_scores()
        self.__database["scores"] = self.scores
        modified_db = json.dumps(self.__database, indent=4)
        with open(DATA_FILE, "w") as f:
            f.seek(0)
            f.write(modified_db)
            f.truncate()

    def sort_scores(self):
        self.scores = {
            key: value
            for key, value in sorted(self.scores.items(), key=lambda item: int(item[1]), reverse=True)
        }

    def load_database(self):
        with open(DATA_FILE) as f:
            database = json.load(f)
        return database

    def tiebreak(self, players):
        counter = -1
        while 1:
            UI.show_round(counter)
            points = []
            for player in players:
                points.append(player.roll(-1))
            UI.show_state(players, points)
            if len(set(points)) == len(points):
                score = max(points)
                winner = players[points.index(score)]
                return winner
            UI.press_to_continue()
            UI.clear()
            counter -= 1

    def get_winner(self):
        largest = -math.inf
        tiebreaker_players = []
        for player in self._players:
            if player.total_score >= largest:
                if player.total_score == largest:
                    tiebreaker_players.append(potential_winner)
                    tiebreaker_players.append(player)
                potential_winner = player
                largest = player.total_score
                potential_winner = player
        if len(tiebreaker_players) > 0:
            winner = self.tiebreak(tiebreaker_players)

        else:
            winner = potential_winner
        return winner

    def play(self):
        for i in range(self.num_round):
            UI.show_round(i + 1)
            points = []
            for player in self._players:
                UI.whose_turn(player.name)
                dice_list = []
                for n in range(self.num_dice):
                    UI.ask_to_roll()
                    dice_list.append(player.roll(n + 1))
                score = player.calc_score(dice_list)
                points.append(score)
            UI.show_state(self._players, points)
            UI.press_to_continue()
            UI.clear()

    def main(self):
        UI.clear()
        if self.init_players():
            self.play()
            winner = self.get_winner()
            UI.show_final_result(winner)
            self.modify_database(winner)
            UI.show_podium(self.scores)


class Player:

    def __init__(self, name, total_score=0):
        self.name = name
        self.total_score = total_score

    def roll(self, n):
        point = random.randint(1, 6)
        self.total_score += point
        UI.show_die(self, point, n)
        return point

    def calc_score(self, dice_list):
        score = sum(dice_list)
        bonus = self.get_bonus(score)
        self.total_score += bonus
        extra = 0
        if len(set(dice_list)) == 1:
            extra = self.roll(-2)
        self.check_if_zero()
        return score + bonus + extra

    def get_bonus(self, score):
        bonus = 0
        if score % 2 == 0:
            bonus += 10
        else:
            bonus -= 5
        return bonus

    def check_if_zero(self):
        if self.total_score < 0:
            self.total_score = 0


if __name__ == "__main__":
    new_game = Game()
    new_game.main()
