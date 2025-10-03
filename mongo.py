import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import discord
from discord.ext import commands

uri = os.getenv("mongodb")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["pvp"]

try:
    client.admin.command("ping")
    print("[Mongo] ping OK")
except Exception as e:
    print(f"[Mongo] ping FAILED: {e!r}")

def setuservar(var: str, userid: str, amt: int):
    userid = str(userid)
    db.users.update_one(
        {"_id": userid},
        {"$inc": {var: amt}},
        upsert=True
    )

def changeuservar(var: str,  userid: str, amt):
    userid = str(userid)
    db.users.update_one(
        {"_id": userid},
        {"$set": {var: amt}},
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

def resetuservar(var: str, userid: str):
    userid = str(userid)
    db.users.update_one(
        {"_id": userid},
        {"$set": {var: 0}},
        upsert=True
    )

def ccreateclan(clanname: str, userid: str):
    clanfind = db.clans.find_one({"_id": clanname})
    if clanfind is not None:
        return "Clan already exists"
    if userinclan(userid) is not None:
        return "User is already in a clan"
    db.clans.update_one(
        {"_id": clanname},
        {"$push": {"members": {"userid": userid, "rank": "Owner", "points": 0}}},
        upsert=True
    )
    return f"You created the clan {clanname}, to view your clan use -clan"

def userinclan(userid: str) -> str | None:
    clanfind = db.clans.find_one({
        "members.userid": userid},
        {"_id": 1})
    
    if clanfind:
        return clanfind["_id"]
    else:
        return None
    
def clanexists(clanname: str):
    clanfind = db.clans.find_one(
        {"_id": clanname}
    )
    if clanfind:
        return True
    else:
        return False
    
def setuserclan(clan: str, userid: str) -> str:
    if not clanexists(clan):
        return "Clan does not exist"
    if not userinclan(userid):
        return "You are already in a clan, leave your old one if you want to join a new one"
    db.clans.update_one(
        {"_id": clan},
        {"$push": {"members": {"userid": userid, "rank": "Member", "points": 0}}},
        upsert=True
    )
    return f"<@{userid}> joined {clan}"

def lb(var: str, amt: int):
    a = ""
    top = db.users.find().sort(var, -1).limit(amt)
    for rank, user in enumerate(top, start=1):
        username = user.get("username", "Unknown")
        value = user.get(var, 0)
        

        a += f"#{rank} - {username} - {value}\n"
    return a


def getlbspot(var: str, userid: str):
    userid = str(userid)
    user = db.users.find_one(
        {"_id": userid}
    )
    rank = db.users.count_documents(
        {var: {"$gt": user[var]}}) + 1
    return rank