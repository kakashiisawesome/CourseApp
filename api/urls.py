from django.urls import path
from .views import *

urlpatterns = [
    path('courses/<int:pk>/', CourseDetail.as_view()),
    path('courses/all/', CourseList.as_view()),
    path('courses/create/', CourseCreate.as_view()),
    path('courses/enroll/<int:course_id>/', EnrollInCourse.as_view()),
    path('courses/delist/<int:course_id>/', DelistFromCourse.as_view()),
    path('courses/enrollments/', GetEnrolledCourses.as_view()),
    path('courses/<int:course_id>/users/', GetEnrolledUsers.as_view()),
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
]