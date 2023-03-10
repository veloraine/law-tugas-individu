from rest_framework.decorators import api_view
from course_calculator.utils import response, validate_body, validate_params
from .models import *
from rest_framework import status
from course_calculator.serializers import *

# Create your views here.
@api_view(['POST'])
def create_course(request):
    # only admin can create course
    if request.user.is_superuser:
        is_valid = validate_body(request, ['name', 'code', 'description', 'program', 'semester', 'sks'])

        if is_valid != None:
            return is_valid
        
        name = request.data.get('name')
        code = request.data.get('code')
        description = request.data.get('description')
        program = request.data.get('program')
        semester = request.data.get('semester')
        sks = request.data.get('sks')

        course = Course.objects.create(name=name, code=code, description=description, program=program, semester=semester, sks=sks)
        return response(data=CourseSerializer(course).data, status=status.HTTP_201_CREATED)
    else:
        return response(error="You are not allowed to create course", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def get_all_course(request):
    courses = Course.objects.all()
    return response(data=CourseSerializer(courses, many=True).data , status=status.HTTP_200_OK)

@api_view(['GET'])
def get_course_by_id(request):
    is_valid = validate_params(request, ['course_id'])

    if is_valid != None:
        return is_valid

    course_id = request.query_params.get('course_id')
    course = Course.objects.filter(id=course_id).first()

    if course == None:
        return response(error="Course not found", status=status.HTTP_404_NOT_FOUND)

    return response(data=CourseSerializer(course).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_calculator(request):
    is_valid = validate_body(request, ['course_id'])

    if is_valid != None:
        return is_valid

    course_id = request.data.get('course_id')
    course = Course.objects.filter(id=course_id).first()

    if course == None:
        return response(error="Course not found", status=status.HTTP_404_NOT_FOUND)
    
    if Calculator.objects.filter(course=course).first() != None:
        return response(error="Calculator for this course already exists", status=status.HTTP_400_BAD_REQUEST)

    calculator = Calculator.objects.create(user=request.user, course=course)
    return response(data=CalculatorSerializer(calculator).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_calculator_by_id(request):
    is_valid = validate_params(request, ['calculator_id'])

    if is_valid != None:
        return is_valid

    calculator_id = request.query_params.get('calculator_id')
    calculator = Calculator.objects.filter(id=calculator_id).first()

    if calculator == None:
        return response(error="Calculator not found", status=status.HTTP_404_NOT_FOUND)

    calculator.delete()
    return response(data="Calculator deleted", status=status.HTTP_200_OK)

@api_view(['GET'])
def get_calculator_by_user(request):
    calculators = Calculator.objects.filter(user=request.user)
    return response(data=CalculatorSerializer(calculators, many=True).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_score_component(request):
    is_valid = validate_body(request, ['calculator_id', 'name', 'weight', 'score'])

    if is_valid != None:
        return is_valid

    calculator_id = request.data.get('calculator_id')
    calculator = Calculator.objects.filter(id=calculator_id).first()

    if calculator == None:
        return response(error="Calculator not found", status=status.HTTP_404_NOT_FOUND)

    name = request.data.get('name')
    weight = request.data.get('weight')
    score = request.data.get('score')

    score_component = ScoreComponent.objects.create(calculator=calculator, name=name, weight=weight, score=score)

    calculator.total_score += weight * score / 100
    calculator.total_percentage += weight
    calculator.save()

    return response(data=ScoreComponentSerializer(score_component).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_score_component_by_calculator(request):
    is_valid = validate_params(request, ['calculator_id'])

    if is_valid != None:
        return is_valid

    calculator_id = request.query_params.get('calculator_id')
    calculator = Calculator.objects.filter(id=calculator_id).first()

    if calculator == None:
        return response(error="Calculator not found", status=status.HTTP_404_NOT_FOUND)

    score_components = ScoreComponent.objects.filter(calculator=calculator)
    return response(data=ScoreComponentSerializer(score_components, many=True).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_score_component_by_id(request):
    is_valid = validate_params(request, ['score_component_id'])

    if is_valid != None:
        return is_valid

    score_component_id = request.query_params.get('score_component_id')
    score_component = ScoreComponent.objects.filter(id=score_component_id).first()

    if score_component == None:
        return response(error="Score component not found", status=status.HTTP_404_NOT_FOUND)
    
    calculator = score_component.calculator
    calculator.total_score -= score_component.score * score_component.weight / 100
    calculator.total_percentage -= score_component.weight
    calculator.save()

    score_component.delete()
    return response(data="Score component deleted", status=status.HTTP_200_OK)