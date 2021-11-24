from django.contrib import admin
from .models import Class, College, Select, Student, ScoreTable, Teacher, Teach

# Register your models here.

admin.site.register(Class)
admin.site.register(College)
admin.site.register(Select)
admin.site.register(Student)
admin.site.register(ScoreTable)
admin.site.register(Teacher)
admin.site.register(Teach)
