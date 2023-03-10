from django.contrib import admin
from .models import Course, Calculator, ScoreComponent

# Register your models here.

admin.site.register(Course)
admin.site.register(Calculator)
admin.site.register(ScoreComponent)
