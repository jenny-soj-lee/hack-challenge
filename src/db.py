from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.event import listen

db = SQLAlchemy()

course_day_association = db.Table('course_days',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'))
)


#classes
class Course(db.Model):
    """
    
    Course class where the fields are code, name, start_time, end_time, and
    days
    
    """
    __tablename__ = "course"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    days = db.relationship('Day', secondary=course_day_association, back_populates='courses')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


    def __init__(self, **kwargs):
        self.code=kwargs.get("code", "")
        self.name= kwargs.get("name", "")
        self.user_id= kwargs.get("user_id")
        self.days= kwargs.get("days", "")
        self.start_time= kwargs.get("start_time", "")
        self.end_time= kwargs.get("end_time", "")


    def serialize(self):
        """
        Serialize a course object, controlling the depth of user and day serialization.
        """
        return  {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "user": User.query.filter_by(id=self.user_id).first().name,
            "days": [day.day_name for day in self.days],
            "start_time": self.start_time,
            "end_time": self.end_time
        }
    
    def simple_serialize(self):
        """
        Serialize a course object, without days field
        """

        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time
        }


class User(db.Model):
  
  """
  Creates User class with fields name and courses
  """
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
  name = db.Column(db.String, nullable=False)
  courses = db.relationship('Course', cascade="delete")


  def __init__(self, **kwargs):
      """
      initalizes name field
      """
      self.name = kwargs.get("name")

  def serialize(self):
        """ Serialize a user object """
        return {
            "id": self.id,
            "name": self.name,
            "courses": [course.simple_serialize() for course in self.courses]
        }

class Day(db.Model):
    """
    Creates Day class with fields day_name and courses
    """
    __tablename__ = "day"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_name = db.Column(db.Integer, nullable=False)
    courses = db.relationship('Course', secondary=course_day_association, back_populates='days')

    def __init__(self, **kwargs):
        self.day_name=kwargs.get("day_name", "")

    def serialize(self, simple=False):
        """
        Serialize a day object. If 'simple' is True, avoid detailed serialization of related courses.
        """
        data = {
            "id": self.id,
            "day_name": self.day_name
        }
        if not simple: 
            data['courses'] = [course.serialize() for course in self.courses]
        return data

#Note:
#course data
#Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6, Sunday=7


















