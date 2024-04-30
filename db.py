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


course_day_association = db.Table('course_days',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
)



class Day(db.Model):
    """
    Day Model for scheduling purposes
    """

    __tablename__ = "day"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)  
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))  
    courses = db.relationship('Course', secondary='course_day_association', back_populates='days')

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize a day object, potentially including time slots
        """
        return {
            "id": self.id,
            "name": self.name,
        }







