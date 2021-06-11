from tinydb import TinyDB, Query

db = TinyDB('db.json')

def addEvent(event):
  return db.insert(event)

def getEvent(id):
  event = db.get(None, int(id))
  return event