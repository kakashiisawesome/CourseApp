from django.db import models
from django.contrib.auth.models import User


class SiteUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    is_educator = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField()
    educator = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='courses', null=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='enrollments', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', null=True)