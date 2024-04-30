from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "user"
  name = db.Column(db.String, nullable = False)
  past_courses = db.relationship("Past Courses", cascade = "delete")
  def __init__(self, **kwargs):
    self.name = kwargs.get("name")
  def simple_serialize(self):
    return {
      "name": self.name,
      "past courses": [c.serialize() for c in self.past_courses]
    }
  
