from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

db = firestore.client()

# List all root-level collections
collections = db.collections()

print("Collections in Firestore:")
for collection in collections:
    print(collection.id)

@app.get("/get-bowler-names")
def get_bowler_names():
    try:
        docs = db.collection("ball_ID").stream()
        result = []

        for doc in docs:
            data = doc.to_dict()
            bowler = data.get("bowlerName", "N/A")
            result.append({"ball_id": doc.id, "bowlerName": bowler})

        return {"bowlers": result}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "API + Firebase is working!"}
