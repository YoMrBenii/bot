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
    if not user:
        return 0
    val = user.get(var, 0)
    return 0 if val is None else val
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
def mlb(var: str, amt: int):
    a = "**Weekly rankings\n**"
    top = db.users.find().sort(var, -1).limit(amt)
    for rank, user in enumerate(top, start=1):
        username = user.get("username", "Unknown")
        value = user.get(var, 0)
        

        a += f"#{rank} - {username} - {value}\n"
    return a
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
    cursor = db.users.find({}, {"_id": 1, var: 1})
    scores = [(d["_id"], (d.get(var) or 0)) for d in cursor]
    scores.sort(key=lambda t: t[1], reverse=True)
    for idx, (uid, _) in enumerate(scores, start=1):
        if uid == userid:
            return idx
    return 0
def jobupdate(job: str, userid: str, amt: str):
    userid = str(userid)
    db.jobs.update_one(
        {"_id": job},
        {"$push": {"member": {"userid": userid, "salary": amt}}},
        upsert=True
    )
def ping_db() -> bool:
    client.admin.command("ping")
    return True
def resetallusers(var: str):
    db.users.update_many(
        {},
        {"$set": {var: 0}}
    )

def top1lb(var: str):
    id = ""
    top = db.users.find().sort(var, -1).limit(1)
    for user in enumerate(top, start=1):
        id = user.get("_id", "Unknown")  
    return id

def top1lbvalue(var: str):
    value = ""
    top = db.users.find().sort(var, -1).limit(1)
    for user in enumerate(top, start=1):
        value = user.get(var, "Unknown")  
    return value
def setservervar(var: str, amt: str):
    db.server.update_one(
        {"_id": "pvp"},
        {"$inc": {var: amt}},
        upsert=True
    )

def changeservervar(var: str, amt):
    db.server.update_one(
        {"_id": "pvp"},
        {"$set": {var: amt}},
        upsert=True
    )

def getservervar(var: str):
    a = db.server.find_one(
        {"_id": "pvp"}
    )
    if a is None:
        return 0
    b = a.get(var, 0)
    return b
