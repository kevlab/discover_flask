from app import db
from models import BlogPost

db.create_all()

db.session.add(BlogPost("Good", "I\'m good."))
db.session.add(BlogPost("Well", "Hello world."))
db.session.add(BlogPost("POSTGRES", "Hello from postgres."))

db.session.commit()
