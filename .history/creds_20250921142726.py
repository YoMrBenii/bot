import firebase_admin
from firebase_admin import credentials, firestore
import os, json
import discord 
from discord.ext import commands
cred_json = os.getenv("fbcreds")
if cred_json:
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("serviceAccouontKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def getuservar(var: str, userid: str):
    userid = str(userid)
    ref = db.collection("users").document(userid)

    value = ref.get()
    if value.exists:
        data = value.to_dict()

        return data.get(var, 0)
    else:
        ref.set({})
        return 0

def setuservar(var: str, userid: str, amt: int = 0):
    userid = str(userid)
    ref = db.collection("users").document(userid)
    value = ref.get()
    
    if value.exists:
        ref.update({var: firestore.Increment(amt)})
    else:
        ref.set({var: firestore.Increment(amt)})

def resetuservar(var: str, userid: str):
    userid = str(userid)
    ref = db.collection("users").document(userid)
    value = ref.get()
    if value.exists:
        ref.update({var: 0})
    else:
        ref.set({var: 0})

def setuserclan(clan: str, userid: str) -> bool:
    userid = str(userid)
    ref = db.collection("clans").document(clan)
    value = ref.get()
    ref.set({
        userid: {
            "rank": "member",
            "points": 0
        }
    })
    return True
    

def find_user_clan(user_id: str) -> str | False:
    user_id = str(user_id)
    clans_ref = db.collection("clans")
    clans = clans_ref.stream()

    for clan in clans:
        data = clan.to_dict()

        if user_id in data:
            return clan.id

    return False

def createclan(clanname: str, userid: str):
    pass


def clanexists(clan: str) -> bool:
    clansref = db.collection("clans")
    clans = clansref.stream()
    for e in clans:
        if e.id == clan:
            return True
        return False
    