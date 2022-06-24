from http import client
import pymongo
import certifi

con_str = "mongodb+srv://hai:123@cluster0.4nuyh.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("haidb")
