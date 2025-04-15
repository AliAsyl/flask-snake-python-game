from database.db import Database



class Model:
    def __init__(self, table):
        self.table = table

class Player(Model):
    def __init__(self, name, total_score=0):
        super().__init__("players")

class GameRecord(Model):
    def __init__(self, player_anme, score=0, collected_berries=0):
        super().__init__("scores")
        