import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = os.getenv("mongodb")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["pvp"]


def setuservar(var: str, userid: str, val: int):
    userid = str(userid)
    db.users.update_one(
        {"_id": userid},
        {"$inc": {var: val}},
        upsert=True
    )

def getuservar(var: str, userid: str):
    users = db["users"]
    userid = str(userid)
    user = users.find_one({"_id": userid})
    if user is None:
        return 0
    val = user.get(var, 0)
    return val
