from random import random

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import ConfirmCode

from users.serializers import (LoginSerializer,
                               RegisterSerializer,
                               UserSerializer)


@api_view(['POST'])
def login(request):
    # 0 - валидация
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 2 - найти пользователя в базе данных
    user = authenticate(**serializer.data)  # serializer.data -> {username:password}
    ConfirmCode.objects.create(user=user)
    # 3 - создать токен
    if user:
        token, created = Token.objects.get_or_create(user=user)

        # 4 - отправить токен
        return Response({'token': token.key})
    return Response({'ERROR': 'WRONG CREDENTIALS'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(
        {'massage': 'You have been successfully logged out.'},
        status=200
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({'data': serializer.data}, status=200)




@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = ''.join(random.choice('1234567890')for _ in range(6))
    user = User.objects.create_user(is_active=False, **serializer.data)
    ConfirmCode.objects.create(user=user, code=code)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'data': serializer.data}, status=201)


@api_view(['POST'])
def confirm(request):
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
    return Response({'massage'})

