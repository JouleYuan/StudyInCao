from flask import Blueprint
from flask_restful import Api
from resources import auth, user, student, teacher, course

routes = Blueprint('routes', __name__)

api = Api(routes)

api.add_resource(auth.Login, '/login')
api.add_resource(auth.ForgotPassword, '/forgot_password')
api.add_resource(auth.ResetPassword, '/reset_password')

api.add_resource(user.AllUsers, '/user')
api.add_resource(user.User, '/user/<string:id>')
api.add_resource(user.Password, '/user/<string:id>/password')
api.add_resource(user.Question, '/user/<string:id>/question')

api.add_resource(student.AllStudents, '/student')
api.add_resource(student.Student, '/student/<string:id>')
api.add_resource(student.StudentDetail, '/student/<string:id>/detail')

api.add_resource(teacher.AllTeachers, '/teacher')
api.add_resource(teacher.Teacher, '/teacher/<string:id>')
api.add_resource(teacher.TeacherDetail, '/teacher/<string:id>/detail')

api.add_resource(course.AllCourses, '/course')
api.add_resource(course.PostCourse, '/course')
api.add_resource(course.Course, '/course/<int:id>')
api.add_resource(course.CourseDetail, 'course/<int:id>/detail')
