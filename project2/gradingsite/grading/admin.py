from django.contrib import admin

# Register your models here.
from .models import Instructor, Course, Student, Assignment, Question

admin.site.register(Question)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Assignment)

