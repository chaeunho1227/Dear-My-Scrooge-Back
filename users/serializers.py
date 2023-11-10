from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserJWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False,
    )

    password1 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['id', 'email', 'nickname', 'password', 'password1']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'],
            nickname=self.validated_data['nickname'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user already exists")

        password = data.get('password', None)
        password1 = data.get('password1', None)

        if password != password1:
            raise serializers.ValidationError("Passwords must match")
        data.pop('password2', None)
        return data



class UserJWTLoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False,
    )
    email = serializers.CharField(
        required=True,
    )

    nickname = serializers.CharField(
        required=False,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta(object):
        model = User
        fields = ['id', 'email', 'nickname', 'password']
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("user account not exist")

        return data

class UserNameSerializer(serializers.ModelSerializer):

        class Meta(object):
            model = User
            fields = ['id', 'nickname', 'view_cnt']