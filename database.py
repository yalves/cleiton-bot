from tinydb import TinyDB, Query

db = TinyDB('db.json')

def addEvent(event):
  return db.insert(event)

def getEvent(id):
  event = db.get(None, int(id))
  return event

def getEventsByDateTime(date):
  events = db.search(Query().datetime == str(date))
  return events

def addUserToEvent(user, id):
  Events = Query()
  event = db.search(Events.id == id)[0]
  users = event['users']
  if user.id not in users:
    users.append(user.id)
    db.update({'users': users}, Events.id == id)

def removeUserFromEvent(user, id):
  Events = Query()
  event = db.search(Events.id == id)[0]
  users = event['users']
  if user.id in users:
    users.remove(user.id)
    db.update({'users': users}, Events.id == id)

  # else:
  #   print("entrou no else")    
  #   db.update({'users': [user.id]}, Events.id == id)
    # db.update({'users': [user.id]}, db.get(None, int(id)))

