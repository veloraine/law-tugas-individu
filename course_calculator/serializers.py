from rest_framework import serializers
from calculator.models import * 

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'program', 'semester', 'sks']

class CalculatorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    course_name = serializers.SerializerMethodField('get_course_name')

    class Meta:
        model = Calculator
        fields = ['id', 'user', 'course_name', 'total_score', 'total_percentage']

    def get_user(self, obj):
        return obj.user.username

    def get_course_name(self, obj):
        return obj.course.name

class ScoreComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreComponent
        fields = ['id', 'calculator', 'name', 'weight', 'score']

