from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import generics
from .serializers import UserRegistrationSerializer
import logging




class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Create response
            response = JsonResponse({"message": "Login successful!"})

            # Set access and refresh tokens in cookies
            response.set_cookie(
                key='access_token', 
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Lax'  # CSRF protection
            )
            response.set_cookie(
                key='refresh_token', 
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        # Remove the access and refresh tokens from cookies
        response = Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        
        # Clear cookies
        response.delete_cookie('access_token')  # Name of your access token cookie
        response.delete_cookie('refresh_token')  # Name of your refresh token cookie
        
        return response




logger = logging.getLogger(__name__)  

class ExampleView(APIView):
    def get(self, request):
        logger.info("GET request received at ExampleView.")
        try:
          
            data = {"message": "Success"}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("An error occurred: %s", e)  
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
