from rest_framework import serializers
from accounts.models import NewUser


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'first_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'username', 'password']
#
#     def create(self, validate_data):
#         user_password = validate_data.get('password', None)
#         db_instance = self.Meta.model(email=validate_data.get('email'), username=validate_data.get('username'))
#         db_instance.set_password(user_password)
#         db_instance.save()
#         return db_instance
#
#
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=100)
#     password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
#     # token = serializers.CharField(max_length=255, read_only=True)