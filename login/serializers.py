
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# from django.contrib.auth.validators import UnicodeUsernameValidator  # Import UnicodeUsernameValidator for username validation
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Define the username validator
    # username_validator = UnicodeUsernameValidator()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'last_login', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'read_only': True}
        }

    def validate_username(self, value):
        # Add username validation logic here
        # if not self.username_validator(value):
        #     raise ValidationError('Username contains invalid characters.')
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise ValidationError('This username is already in use.')
        return value

    def validate_password(self, value):
        # Add password validation logic here
        validate_password(value)
        return value

    def validate_email(self, value):
        # Add email validation logic here if needed
        # Example: Check if the email format is valid
        from django.core.validators import validate_email
        validate_email(value)
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



# from rest_framework import serializers
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'password', 'last_login', 'is_active']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'last_login': {'read_only': True}
#         }

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user
