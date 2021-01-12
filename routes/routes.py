from flask import Blueprint
from flask_restful import Api
from resources import auth, user, student, teacher, course, grade,\
    courseList, chapter, resource, image, post, reply, file, homework, notification

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
api.add_resource(course.CourseClassification, '/course/classification/<string:classification>')
api.add_resource(course.CourseSearch, 'course/search/<string:keyword>')
api.add_resource(course.CourseDetail, 'course/<int:id>/detail')
api.add_resource(course.CourseStudent, 'course/<int:course_id>/<string:student_id>')

api.add_resource(courseList.StudentCourseList, 'courseList/student/<string:student_id>')
api.add_resource(courseList.TeacherCourseList, 'courseList/teacher/<string:teacher_id>')

api.add_resource(grade.CourseStudentGrade, 'grade/<int:course_id>/<string:student_id>')
api.add_resource(grade.CourseGrade, 'grade/course/<int:course_id>')
api.add_resource(grade.StudentGrade, 'grade/student/<string:student_id>')

api.add_resource(chapter.AllChapter, 'chapter')
api.add_resource(chapter.CourseChapter, 'chapter/<int:course_id>')
api.add_resource(chapter.Chapter, 'chapter/<int:course_id>/<int:no>')

api.add_resource(resource.AllResource, 'resource')
api.add_resource(resource.CourseResource, 'resource/course/<int:course_id>')
api.add_resource(resource.ChapterResource, 'resource/chapter/<int:chapter_id>')
api.add_resource(resource.IdResource, 'resource/id/<int:id>')

api.add_resource(homework.AllHomework, 'homework')
api.add_resource(homework.CourseHomework, 'homework/course/<int:course_id>')
api.add_resource(homework.ChapterHomework, 'homework/chapter/<int:chapter_id>')
api.add_resource(homework.IdHomework, 'homework/id/<int:id>')

api.add_resource(image.CourseImage, 'image/course/<int:id>')
api.add_resource(image.StudentImage, 'image/student/<string:id>')
api.add_resource(image.TeacherImage, 'image/teacher/<string:id>')

api.add_resource(file.ResourceFile, 'file/resource/<int:id>')

api.add_resource(post.Posts, 'posts/<int:course_id>')
api.add_resource(post.Post, 'post/<int:post_id>')

api.add_resource(reply.Replies, 'replies/<int:post_id>')
# api.add_resource(reply.Reply, 'reply/<int:reply_id>')

api.add_resource(notification.StudentNotification, 'notification/<string:student_id>')
