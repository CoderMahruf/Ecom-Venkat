from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user':user}