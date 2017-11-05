from app import db
from app import Note

db.create_all()
seed = Note("First Note!", "This ia a first note!")
seed.save()

