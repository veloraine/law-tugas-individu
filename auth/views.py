from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from course_calculator.utils import response
from course_calculator.utils import validate_body
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        is_valid = validate_body(request, ['username', 'email', 'password1', 'password2'])

        if is_valid != None:
            return is_valid
        
        if User.objects.filter(username=request.data.get('username')).exists():
            return response(error="Username already exists", status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('password1') != request.data.get('password2'):
            return response(error="Passwords do not match", status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password1')

        User.objects.create_user(username = username, email = email, password = password)
        print(f"User {username} created")
        return response(data="Registration successful", status=status.HTTP_201_CREATED)

    else:
        return response(error="Method not allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
