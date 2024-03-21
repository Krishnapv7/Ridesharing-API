from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer
from .models import CustomUser

class RegisterUserView(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=[permissions.AllowAny]
    
class LoginUserView(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        
        user=authenticate(username=username,password=password)
        
        if user:
            token,created=Token.objects.get_or_create(user=user)
            return Response({'token':token.key})
        else:
            return Response({'error':'invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
