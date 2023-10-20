from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']

    def create(self, validate_data):
        user_password = validate_data.get('password', None)
        db_instance = self.Meta.model(email=validate_data.get('email'), username=validate_data.get('username'))
        db_instance.set_password(user_password)
        db_instance.save()
        return db_instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
    # token = serializers.CharField(max_length=255, read_only=True)