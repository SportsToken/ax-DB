import pymongo
from pymongo import MongoClient

# get client
cluster = MongoClient("mongodb+srv://AXMarkets:<password>@axmarkets.1hesm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# get db
db = cluster['AXMarkets']
# get collection
collection = db['AXMarkets']

collection.insert_one({})