from database.db import Database



class Model:
    def __init__(self, table):
        self.table = table

    def model_create(self):
        Database.create(self.table, self.get_as_json())

    def model_update(self):
        Database.update(self.table, self.get_as_json())

    def get_as_json(self):
        return {}


class Player(Model):
    def __init__(self, name):
        super().__init__("players")
        self.name = name
        self.total_score = 0
    
    def get_as_json(self):
        return {
            'name':self.name,
            'total_score':self.total_score
        }

    def load(self, name):
        result = Database.read(self.table, {'name':name})
        if len(result) == 0:
            self.model_create()
            return
        self.total_score = result['total_score']

    def add_score(self, score):
        self.total_score += score
        self.model_update()
    
class GameRecord(Model):
    def __init__(self, player_name, score, collected_berries):
        super().__init__("scores")
        self.player_name = player_name
        self.score = score
        self.collected_berries = collected_berries

    @staticmethod
    def load(player_name):
        search_results = Database.read(self.table, {'player_name':player_name})
        records = []
        for record in search_results:
            records.append(GameRecord(player_name, record['score'], record['collected_berries']))
        return records