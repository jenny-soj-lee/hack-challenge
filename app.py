import json
from db import db
from flask import Flask, request
from db import Course
from db import User

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# create student
@app.route("/api/user/", methods = ["POST"])
def create_user():
    body = json.loads(request.data)
    new_user = User (
        name = body.get("name")
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

# add a past course
@app.route("/api/user/<int:course_id>/past/", methods =["POST"])
def add_past_course(course_id):
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response("Course not found!")
    user = User.query.filter_by(id = 0).first()
    if user is None:
        return failure_response("User not found!")
    user.past_courses.append(course.serialize())
    return success_response(course.serialize())

# delete a past course
@app.route("/api/user/<int:course_id>/past/", methods = ["DELETE"])
def delete_past_course(course_id):
    #given course id, filter past_courses to see if student has taken course
    #if yes, remove course from list of past_courses
    user = User.query.filter_by(id = 0).first()
    if user is None:
        return failure_response("User not found!")
    


# get all past courses
@app.route("/api/user/past/", methods = ["GET"])
def get_past_courses():
    user = User.query.filter_by(id = 0).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.past_courses_serialize())

# add a current course
@app.route("/api/user/<int:course_id>/current/", methods =["POST"])
def add_current_course(course_id):
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response("Course not found!")
    user = User.query.filter_by(id = 0).first()
    if user is None:
        return failure_response("User not found!")
    user.current_courses.append(course.serialize())
    return success_response(course.serialize())

# get all current courses
@app.route("/api/user/current/", methods = ["GET"])
def get_current_courses():
    user = User.query.filter_by(id = 0).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.current_courses_serialize())

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code = 200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code = 404):
    return json.dumps({"success": False, "error": message}), code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)