import time
import json
from sqlalchemy import and_, func
from db import Course, User, Day,  db
from flask import Flask, request


app = Flask(__name__)
db_filename = "course.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    """
    initalizes day instances from 1 through 7
    """
    for i in range(1,8):
        db.session.add(Day(day_name=i))

    db.session.commit()


def success_response(message, code = 200):
    """
    returns success response where message is a string 
    """
    return json.dumps(message), code

def failure_response(message, code = 404):
    """
    returns failure response where message is an input 
    """
    return json.dumps({ "error": message}), code

@app.route('/api/days/', methods=['GET'])
def get_days():
    """
    get all days instances
    
    """
    days_list=[]
    for day in Day.query.all():
        days_list.append(day.serialize(False))
    return success_response({"courses": days_list})


@app.route('/api/courses/')
def get_courses():
    """
    Endpoint for getting all courses FROM PREPOPULATED SQL DATA
    """

    courses = []
    for course in Course.query.all():
        courses.append(course.serialize())

    if courses:
        return success_response({"courses": courses})
    else:
        return failure_response({"error": "no courses"}), 404



@app.route('/api/courses/add/', methods=['POST'])
def add_course():
    """
    Endpoint for getting adding  course FROM SQL DATA
    """
    body= json.loads(request.data)
   

    if (body.get("code") is None) or (body.get("name") is None) or body.get("days") is None or body.get("start_time") is None or body.get("end_time") is None or  body.get("user_id") is None:
        return failure_response("fill in all fields", 400)

    days = body['days'].split()  # Assuming 'days' is a space-separated string of day numbers
    day_objects = []
    for day in days:
        day_name = Day.query.filter_by(day_name=int(day)).first()
        if  day_name is None:
            day = Day(day_name=int(day_name))
            db.session.add(day_name)  
    
        day_objects.append(day_name)
    db.session.commit()
    print(day_objects)
    # Create the new Course object
    new_course = Course(
        code=body['code'],
        name=body['name'],
        user_id= body["user_id"],
        days=day_objects,  # Assign the day objects list to the days relationship
        start_time=body['start_time'],
        end_time=body['end_time']
    )
    db.session.add(new_course)
    db.session.commit()

    return json.dumps(new_course.serialize()), 201
    


@app.route('/api/courses/<int:id>/', methods=['GET'])
def get_course(id):
    """
    Endpoint for getting specific course FROM PREPOPULATED SQL DATA
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return failure_response("Course not found",404)
    return success_response(course.serialize())


@app.route('/api/suggestedcourses/', methods=['POST'])
def get_suggested_courses():
    """
    Retrieves all courses based on user's input constraints
    """

    body= json.loads(request.data)
    prefix = body.get('prefix')
    days = body.get('days')
    start_time = body.get('start_time')
    end_time = body.get('end_time')

    if not prefix or not start_time or not end_time or days is None:
        return failure_response("Prefix, day, start_time and end_time parameters are required", code=400)

    day_list = days.split()  # Assuming 'days' is a space-separated string of day numbers
    day_ints = []
    for day in day_list:
        day_int = int(day)
        if day_int < 1 or day_int > 7:
            return json.dumps({"error": "Day must be from 1 to 7"}), 400
        day_ints.append(day_int)
  
    courses = Course.query.filter(Course.code.startswith(prefix), Course.start_time >= start_time,  Course.end_time <= end_time).all()

    filtered_courses = []
    for course in courses:
        course_days = set(course.serialize()['days'])  
        if set(day_ints).issubset(course_days):
            filtered_courses.append(course.serialize())

    return success_response({"courses": filtered_courses}, 201)
 
 #create student
@app.route("/api/user/", methods = ["POST"])
def create_user():
     """
     Creates user instance 
     
     """
     body = json.loads(request.data)
     if body.get("name") is None:
         return json.dumps({"error": "fill in name"}), 400
     new_user = User (
         name = body.get("name")
     )
     db.session.add(new_user)
     db.session.commit()
     return json.dumps(new_user.serialize()),201


@app.route("/api/user/")
def get_user():
    """
    Get's user instance where id will always be 1 since theres only one user
    
    """
    user = User.query.filter_by(id=1).first()
    if user is None:
        return failure_response("user not found")
    return success_response(user.serialize())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
