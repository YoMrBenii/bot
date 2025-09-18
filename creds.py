import firebase_admin
from firebase_admin import credentials, firestore
import os, json
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