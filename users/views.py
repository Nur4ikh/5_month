from random import random
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import ConfirmCode
from users.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            ConfirmCode.objects.create(user=user)

            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key})
        return Response({'ERROR': 'WRONG CREDENTIALS'}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(
            {'message': 'You have been successfully logged out.'},
            status=200
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'data': serializer.data}, status=200)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = ''.join(random.choice('1234567890') for _ in range(6))

        user = User.objects.create_user(is_active=False, **serializer.validated_data)
        ConfirmCode.objects.create(user=user, code=code)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'data': serializer.data}, status=201)

class ConfirmView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'ERROR': 'NO CODE'}, status=400)

        code = ConfirmCode.objects.filter(code=code).first()

        if not code:
            return Response({'ERROR': 'NO CODE'}, status=400)

        user = code.user
        user.is_active = True
        user.save()
        code.delete()

        return Response({'message': 'Account has been confirmed'}, status=200)


