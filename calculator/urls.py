from django.urls import path
from .views import *

app_name = "calculator"

urlpatterns = [
    path('course/list', get_all_course, name='course-list'),
    path('course/get', get_course_by_id, name='get-course-by-id'),
    path('course/create', create_course, name='create-course'),
    
    path('calculator/create', create_calculator, name='create-calculator'),
    path('calculator/delete', delete_calculator_by_id, name='delete-calculator-by-id'),
    path('calculator/get', get_calculator_by_user, name='get-calculator-by-user'),

    path('score-component/create', create_score_component, name='create-score-component'),
    path('score-component/get', get_score_component_by_calculator, name='get_score_component_by_calculator'),
    path('score-component/delete', delete_score_component_by_id, name='delete-score-component-by-id'),
]