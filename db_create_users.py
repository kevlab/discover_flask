from app import db
from models import User

db.session.add(User("john", "john@doe.com", "i'll-never-tell"))
db.session.add(User("admin", "ad@min.com", "admin"))

db.session.commit()
