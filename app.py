import time
import json
from db import Course, db
from flask import Flask, request

app = Flask(__name__)
db_filename = "course.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code
def failure_response(message, code=404):
    return json.dumps({"error": message}), code


#routes
@app.route('/api/courses/', methods=['GET'])
def get_courses():
    """
    Endpoint for getting all courses FROM PREPOPULATED SQL DATA
    """
    courses = []
    for course in Course.query.all():
        courses.append(course.serialize())
    return success_response({"courses": courses})

@app.route('/api/courses/<int:id>/', methods=['GET'])
def get_course(id):
    """
    Endpoint for getting specific course FROM PREPOPULATED SQL DATA
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route('/api/courses/<int:id>/', methods=['DELETE'])
def delete_course(id):
    """
    Endpoint for deleting course FROM PREPOPULATED SQL DATA
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())

@app.route('/api/suggestedcourses/', methods=['GET'])
def get_suggested_courses():
    prefix = request.args.get('prefix')
    day = request.args.get('day')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not prefix or not start_time or not end_time or not day:
        return failure_response("Prefix, day, start_time and end_time parameters are required", code=400)

    if int(day)<1 or int(day)>7:
        return failure_response("days needs to be between 1 (Monday) and 7 (Sunday)")
    
    try:
        time.strptime(start_time, '%H:%M') 
        time.strptime(end_time, '%H:%M')
    except ValueError:
        return failure_response("Invalid time format, use 'HH:MM'", code=400)
    
    courses = Course.query.filter(Course.code.startswith(prefix), 
                                  Course.start_time >= start_time, 
                                  Course.end_time <= end_time, 
                                  Course.days.contains(day)).all()
    return success_response({"courses": [course.serialize() for course in courses]})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
