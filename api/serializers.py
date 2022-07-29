from rest_framework import serializers
from .models import SiteUser, Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'description')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True, trim_whitespace=False)

    def create(self, validated_data):
        return SiteUser.objects.create(name=validated_data['name'], phone=validated_data['phone'], is_educator=validated_data['is_educator'])

    class Meta:
        model = SiteUser
        fields = ('password', 'username', 'name', 'phone', 'is_educator')


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('user', 'course')