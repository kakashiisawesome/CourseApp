# CourseApp

- To run the app run `python manage.py runserver`
- A django rest api for a Course learning App where users and educators can sign up and login.  
- A normal user can get the list of all courses and enroll/delist from the courses, and view his/her enrolled courses  
- An educator can list the courses, create a course and delete a course. The educator can also list all the users enrolled into a course  

Following endpoints are available:  


` POST /api/register/` : Sign up for a user (You have to sign up and login before calling any other apis)  

` POST /api/login/` : Login for a user  

` GET /api/logout/` : Logout for a user  

` GET /api/courses/all/` : Returns all available courses  

` GET /api/courses/<int>/` : Returns name and description for a course
{
        "name": "Azure",
        "description": "An Azure course"
}  

` POST /api/courses/create/` : Creates a new course  

` GET /api/courses/delete/<int:course_id>/` : Deletes a course  

` GET /api/courses/enroll/<int:course_id>/` : Enrolls the user in a course  

` GET /api/courses/delist/<int:course_id>/` : Delists the user from a course  

` GET /api/courses/enrollments/` : Returns all the enrolled courses of the user  

` GET /api/courses/<int:course_id>/users/` : Returns all the users that have enrolled in a course  
