from django.contrib import admin
from .models import *

admin.site.register(SiteUser)
admin.site.register(Course)
admin.site.register(Enrollment)