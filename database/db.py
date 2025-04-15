#python-project-5-db-passwd
#s30939

#mongodb+srv://s30939:python-project-5-db-passwd@python-project-5-db.2gpuogz.mongodb.net/?retryWrites=true&w=majority&appName=python-project-5-db


from pymongo import MongoClient

class Database:
    NAME = "python-project-5"
    URI = "mongodb+srv://s30939:python-project-5-db-passwd@python-project-5-db.2gpuogz.mongodb.net/?retryWrites=true&w=majority&appName=python-project-5-db"
    
    DB = None
    
    @staticmethod
    def init():
        client = MongoClient(Database.URI)
        Database.DB = client[Database.NAME]
    @staticmethod
    def create(table, data):
        return Database.DB[table].insert_one(data).inserted_id
    @staticmethod
    def read_all(table):
        return list(Database.DB[table].find())
    @staticmethod
    def read(table, match):
        return list(Database.DB[table].find(match))
    @staticmethod
    def update(table, match, update):
        return Database.DB[table].update_one(
            match,
            {"$set": update}
        )
    @staticmethod
    def delete(table, match):
        return Database.DB[table].delete_one(match)
