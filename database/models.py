from database.db import Database
import datetime


class Model:
    TABLE = ""

    def model_create(self):
        Database.create(self.TABLE, self.get_as_json())

    def model_update(self, match):
        Database.update(self.TABLE, match, self.get_as_json())
    def get_as_json(self):
        return {}


class Player(Model):
    TABLE = "players"
    def __init__(self, name, total_score=0, last_session_time=""):
        super().__init__()
        self.name = name
        self.total_score = total_score
        self.last_session_time = last_session_time
    
    def get_as_json(self):
        return {
            'name':self.name,
            'total_score':self.total_score,
            'last_session_time':self.last_session_time
        }
    @staticmethod
    def get_all_players():
        result = []
        for i in Database.read_all(Player.TABLE):
            result.append(Player(i['name'], i['total_score'], i['last_session_time']))
        return result

    def exists(self):
        return len(Database.read(self.TABLE, {'name': self.name})) > 0

    def load(self):
        result = Database.read(self.TABLE, {'name':self.name})
        if len(result) == 0:
            self.model_create()
            return
        self.total_score = result[0]['total_score']

    def add_score(self, score):
        self.total_score += score
        self.last_session_time = str(datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        self.model_update({'name':self.name})
    
class ScoreRecord(Model):
    TABLE = "scores"
    def __init__(self, player_name, score, collected_berries, board_size):
        super().__init__()
        self.player_name = player_name
        self.score = score
        self.collected_berries = collected_berries
        self.board_size = board_size

    def get_as_json(self):
        return {
            'player_name':self.player_name,
            'score':self.score,
            'collected_berries':self.collected_berries,
            'board_size':self.board_size
        }


    @staticmethod
    def load(player_name):
        search_results = Database.read(ScoreRecord.TABLE, {'player_name':player_name})
        records = []
        for record in search_results:
            print(record)
            records.append(ScoreRecord(player_name, record['score'], record['collected_berries'], record['board_size']))
        return records
    
    def save(self):
        Database.create(ScoreRecord.TABLE, self.get_as_json())