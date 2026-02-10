from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_URI)

print(client.list_database_names())
db = client.naleystogram
users = db.users