import time
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://pushupsGod:drones@cluster0.pdg4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db= client["Drones"]
collection = db["MapData"]
# Issue the serverStatus command and print the results
while True:

    time.sleep(1); 
    pprint(collection.find_one()["Update"])
    if (collection.find_one()["Update"] == 1):
        x = collection.find_one()["Latitude"]
        y = collection.find_one()["Longitude"]
        print(x)
        print(y)
        myquery = {}
        newvalues = { "$set": { "Update": 0 } }
        collection.update_one(myquery, newvalues)

