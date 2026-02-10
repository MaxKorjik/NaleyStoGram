from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://ytgreik_db_user:9AaCxiuZyIVqQ2RO@naleystogram.v98iit4.mongodb.net/?appName=NaleyStoGram'
client = MongoClient(MONGO_URI)

db = client.naleystogram
users = db.users