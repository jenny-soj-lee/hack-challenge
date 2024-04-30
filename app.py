import datetime
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

@app.route('/api/plan/', methods=['GET'])
def get_suggested_courses():
    body = json.loads(request.data)
    prefix = body.get('prefix')
    start_time = body.get('start_time')
    end_time = body.get('end_time')

    if not prefix or not start_time or not end_time:
        return failure_response("Prefix, start_time and end_time parameters are required", code=400)

    try:
        start_time = datetime.strptime(start_time, '%H:%M').time()  # assuming time is given as 'HH:MM'
        end_time = datetime.strptime(end_time, '%H:%M').time()
    except ValueError:
        return failure_response("Invalid time format, use 'HH:MM'", code=400)
    
    courses = Course.query.filter(Course.prefix == prefix, Course.start_time >= start_time, Course.end_time <= end_time).all()
    return success_response({"courses": [course.serialize() for course in courses]})

@app.route('/api/plan/<int:id>/', methods=['GET'])
def get_suggested_course(id):
    body = json.loads(request.data)
    prefix = body.get('prefix')
    start_time = body.get('start_time')
    end_time = body.get('end_time')

    if not prefix or not start_time or not end_time:
        return failure_response("Prefix, start_time and end_time parameters are required", code=400)

    try:
        start_time = datetime.strptime(start_time, '%H:%M').time()  # assuming time is given as 'HH:MM'
        end_time = datetime.strptime(end_time, '%H:%M').time()
    except ValueError:
        return failure_response("Invalid time format, use 'HH:MM'", code=400)
    
    course = Course.query.filter_by(id=id).filter(
        Course.prefix == prefix,
        Course.start_time >= start_time,
        Course.end_time <= end_time
    ).first()   

    if not course:
        return failure_response("No suitable course found", code=404)

    return success_response(course.serialize())


    
