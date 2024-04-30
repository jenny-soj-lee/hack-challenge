from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
  __tablename__ = "student"
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.String, nullable = False)
  past_courses = db.relationship("Past Courses", cascade = "delete")
  def __init__(self, **kwargs):
    self.id = kwargs.get("id")
    self.name = kwargs.get("name")
  def simple_serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "past courses": [c.serialize() for c in self.past_courses]
    }
  
