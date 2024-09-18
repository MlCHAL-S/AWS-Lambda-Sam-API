from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient('mongodb+srv://nahciahprah:BUd2NgkyAm6h19vO@mydb.cd8zs.mongodb.net/?retryWrites=true&w=majority&appName=myDB')
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()