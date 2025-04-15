from database.db import Database
import datetime


class Model:
    TABLE = ""

    def model_create(self):
        Database.create(Model.TABLE, self.get_as_json())

    def model_update(self):
        Database.update(Model.TABLE, self.get_as_json())

    def get_as_json(self):
        return {}


class Player(Model):
    TABLE = "players"
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.total_score = 0
        self.last_session_time = ""
    
    def get_as_json(self):
        return {
            'name':self.name,
            'total_score':self.total_score,
            'last_session_time':self.last_session_time
        }

    def load(self):
        result = Database.read(Player.TABLE, {'name':self.name})
        if len(result) == 0:
            self.model_create()
            return
        self.total_score = result['total_score']

    def add_score(self, score):
        self.total_score += score
        self.model_update()
    
class ScoreRecord(Model):
    TABLE = "scores"
    def __init__(self, player_name, score, collected_berries, time):
        super().__init__()
        self.player_name = player_name
        self.score = score
        self.collected_berries = collected_berries
        self.time = time

    def get_as_json(self):
        return {
            'player_name':self.player_name,
            'score':self.score,
            'collected_berries':self.collected_berries,
            'time':self.time
        }


    @staticmethod
    def load(player_name):
        search_results = Database.read(ScoreRecord.TABLE, {'player_name':player_name})
        records = []
        for record in search_results:
            records.append(ScoreRecord(player_name, record['score'], record['collected_berries'], record['time']))
        return records
    
    def save(self):
        Database.create(ScoreRecord.TABLE, self.get_as_json())