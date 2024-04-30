import json
from db import db
from flask import Flask, request
from db import Course
from db import Student

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# add a past course
@app.route("/api/user/<int:course_id>/past/", methods =["POST"])
def add_past_course(course_id):
    course = Course.query.filter_by(id = course_id).first()
    if course is None:
        return failure_response("Course not found!")
    body = json.loads(request.data)
    student_id = body.get("user_id")
    student = Student.query.filter_by(id = student_id).first()
    if user is None:
        return failure_response("User not found!")
    student.past_courses.append(course.serialize())
    return success_response(course.serialize())




db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code = 200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code = 404):
    return json.dumps({"success": False, "error": message}), code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)