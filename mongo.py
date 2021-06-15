import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.getenv("CONNECTION_STRING"))
db = client["bots"]
collection = db["events"]

def addEvent(event):
  collection.insert_one(event)

def getEvent(id):
  event = collection.find({"id": int(id)})[0]
  return event

def getEventsByDateTime(date):
  events = collection.find({"datetime": str(date)})
  return events

def removeEvent(event):
  collection.delete_one({"id": int(event['id'])})

def addUserToEvent(user, id):
  query = {"id": int(id)}
  event = collection.find(query)[0]
  users = event['users']
  if user.id not in users:
    users.append(user.id)
    newValues = { "$set": { "users": users }}
    collection.update(query, newValues)

def removeUserFromEvent(user, id):
  query = {"id": int(id)}
  event = collection.find(query)[0]
  users = event['users']
  if user.id in users:
    users.remove(user.id)
    newValues = { "$set": { "users": users }}
    collection.update(query, newValues)

