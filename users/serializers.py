from rest_framework import serializers
from django.contrib.auth.models import User
# from users.models import


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(UserValidateSerializer):
    pass


class RegisterSerializer(UserValidateSerializer):
    email = serializers.EmailField(required=False)
    last_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
