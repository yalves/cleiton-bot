from tinydb import TinyDB, Query

db = TinyDB('db.json')

def addEvent(event):
  return db.insert(event)

def getEvent(id):
  event = db.get(None, int(id))
  return event

def addUserToEvent(user, id):
  Events = Query()
  event = db.search(Events.id == id)[0]
  print(event)
  users = event['users']
  print(users)  
  if user.id not in users:
    users.append(user.id)
    print(users)
    db.update({'users': users}, Events.id == id)

  # else:
  #   print("entrou no else")    
  #   db.update({'users': [user.id]}, Events.id == id)
    # db.update({'users': [user.id]}, db.get(None, int(id)))

