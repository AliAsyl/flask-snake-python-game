#python-project-5-db-passwd
#s30939

#mongodb+srv://s30939:python-project-5-db-passwd@python-project-5-db.2gpuogz.mongodb.net/?retryWrites=true&w=majority&appName=python-project-5-db


from pymongo import MongoClient

class Database:
    NAME = "python-project-5"
    URI = "mongodb+srv://s30939:python-project-5-db-passwd@python-project-5-db.2gpuogz.mongodb.net/?retryWrites=true&w=majority&appName=python-project-5-db"
    def __init__(self):
        self.client = MongoClient(Database.URI)
        self.db = self.client[Database.NAME]
        self.scores = self.db["scores"]

    def create_player(self, name):
        score = {
            "name": name,
            "score": 0
        }
        return self.scores.insert_one(score).inserted_id

    def read_all_players(self):
        return list(self.scores.find())

    def update_player_score(self, name, new_score):
        return self.scores.update_one(
            {"name": name},
            {"$set": {"score": new_score}}
        )

    def delete_player(self, name):
        return self.scores.delete_one({"name": name})
