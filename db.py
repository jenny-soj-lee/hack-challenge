from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "user"
  name = db.Column(db.String, nullable = False)
  past_courses = db.relationship("Past Courses", cascade = "delete")
  current_courses = db.relationship("Current Courses", cascade = "delete") 
  def __init__(self, **kwargs):
    self.name = kwargs.get("name")
  def simple_serialize(self):
    return {
      "name": self.name,
      "past courses": [p.serialize() for p in self.past_courses],
      "current courses": [c.serialize() for c in self.current_courses]
    }
  def past_courses_serialize(self):
    return {
      "past courses": [p.serialize() for p in self.past_courses]
    }  
  def current_courses_serialize(self):
    return {
      "current courses": [c.serialize() for c in self.current_courses]
    }  
