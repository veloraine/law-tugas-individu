from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    sks = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return self.name
    

class Calculator(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    course = models.ForeignKey(Course, on_delete=CASCADE)
    total_score = models.FloatField(default=0)
    total_percentage = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + " - " + self.course.name

class ScoreComponent(models.Model):
    calculator = models.ForeignKey(Calculator, on_delete=CASCADE)
    name = models.TextField()
    weight = models.FloatField()
    score = models.FloatField()

    def __str__(self):
        return self.calculator.course.name + " - " + self.name