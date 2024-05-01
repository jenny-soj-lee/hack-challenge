from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.event import listen

db = SQLAlchemy()


#classes
class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    days = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=True) 
    end_time = db.Column(db.String, nullable=True)    

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")
        self.days = kwargs.get("days", "")
        self.start_time = kwargs.get("start_time", None)
        self.end_time = kwargs.get("end_time", None)

    def serialize(self):
        """
        Serialize a course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "days": self.days,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

#course data
#Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6, Sunday=7

@event.listens_for(Course.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Course(code='CS 1110',       name='Programming with Python', days='1 3 5', start_time='09:00', end_time='10:00'))
    db.session.add(Course(code='CS 2110',       name='Programming with Java', days='2 4 5', start_time='10:00', end_time='11:00'))
    db.session.add(Course(code='MATH 1910',     name='Calculus II', days='1 2 3', start_time='11:00', end_time='12:00'))
    db.session.add(Course(code='MATH 1920',     name='Calculus III', days='5 6 7', start_time='12:00', end_time='13:00'))
    db.session.add(Course(code='PHYS 1112',     name='Physics I', days='3 5', start_time='13:00', end_time='14:00'))
    db.session.add(Course(code='PHYS 2213',     name='Physics II', days='1 3', start_time='14:00', end_time='15:00'))
    db.session.commit()
    print('course initial values created')


