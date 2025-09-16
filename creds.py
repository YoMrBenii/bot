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
    ref = db.reference(f"users/{userid}/{var}")
    value = ref.get()
    if value is None:
        return 0
    return value