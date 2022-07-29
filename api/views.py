from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreate(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        if not request.user.siteuser.is_educator:
            return Response('Only Educators can create courses', status=400)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Course created successfully')
        else:
            return Response(serializer.errors, status=400)


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response('User with that username already exists', status=400)

            # Create User object to associate with the SiteUser
            user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            site_user = serializer.save()
            site_user.user = user
            site_user.save()
            return Response('User created successfully')
        else:
            return Response(serializer.errors, status=400)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        if request.user.is_authenticated:
            return Response('User is already logged in', status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response('Login success')
        else:
            return Response('Invalid user credentials', status=400)


class LogoutUser(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response('Logged out successfully')

# Enroll in a course
class EnrollInCourse(APIView):
    def get(self, request, course_id, *args, **kwargs):
        if request.user.siteuser.is_educator:
            return Response('Educators cannot enroll into courses', status=400)

        course = get_object_or_404(Course, id=course_id)

        site_user = request.user.siteuser
        enrollment = Enrollment(user=site_user, course=course)
        enrollment.save()
        return Response('Successfully enrolled in course: ' + course.name)

# Delist from a course
class DelistFromCourse(APIView):
    def get(self, request, course_id, *args, **kwargs):
        if request.user.siteuser.is_educator:
            return Response('Educators cannot delist from courses', status=400)

        course = get_object_or_404(Course, id=course_id)
        enrollment = get_object_or_404(Enrollment, course=course, user=request.user.siteuser)
        enrollment.delete()
        return Response('Successfully delisted from course: ' + course.name)


# Returns courses that the user has enrolled in
class GetEnrolledCourses(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.siteuser.is_educator:
            return Response('Educators cannot be enrolled into courses', status=400)

        user = request.user.siteuser
        enrollments = Enrollment.objects.filter(user=user)

        course_names = []
        for item in enrollments:
            course_names.append(item.course.name)

        return Response(course_names)


# Returns the users that have enrolled in a course
class GetEnrolledUsers(APIView):
    def get(self, request, course_id, *args, **kwargs):
        if not request.user.siteuser.is_educator:
            return Response('Only Educators are allowed to view this data', status=400)

        course = get_object_or_404(Course, id=course_id)
        enrollments = Enrollment.objects.filter(course=course)
        user_names = []
        for item in enrollments:
            user_names.append(item.user.name)

        return Response(user_names)