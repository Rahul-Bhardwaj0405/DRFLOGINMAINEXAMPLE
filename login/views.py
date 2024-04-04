
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from rest_framework.permissions import AllowAny
from django.contrib import messages






@api_view(['GET'])
def welcome(request):
    return render(request, 'login/welcome.html', {'user': request.user})

@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, 'Registration successful!')
            return redirect('login') 
        else:
            # Extract validation errors from serializer and display them in the frontend
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('register_user')  # Redirect back to the registration page
    return render(request, 'login/register.html')
# def register_user(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # Optionally, add success message to be displayed on successful registration
#             messages.success(request, 'Registration successful!')
#             return redirect('login') 
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return render(request, 'login/register.html')

@api_view(['GET', 'POST'])  # Allow GET requests for rendering the login form
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username) # Here in models.py instead of email attribute username should be used in the future.
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return redirect('guitar_info')

        return render(request, 'login/login.html', {'error': 'Invalid credentials'})

    # Render the login form for GET requests
    return render(request, 'login/login.html')



@api_view(['POST'])
@permission_classes([AllowAny])  # Allow both authenticated and unauthenticated users
def user_logout(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                # Delete the user's token to logout
                request.user.auth_token.delete()
            return redirect('login')  # Redirect to the login page after logout
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Handle GET requests or invalid requests by redirecting to the login page
    return redirect('login')


@api_view(['GET'])
def guitar_info(request):
    return render(request, 'login/guitar_info.html')