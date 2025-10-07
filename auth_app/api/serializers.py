from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers



class UserProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ["id","email","username"]


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration handling full name parsing and password validation.
    Ensures email uniqueness and matching passwords before creating a new user.
    """
    username = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        

    def validate_email(self, value):

        """
        Ensures that the provided email is not already in use.
        Raises a validation error if a duplicate is found.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):

        """
        Raises an error if passwords do not match or other validation fails.
        """
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        account = User(
            email=self.validated_data['email'], 
            username=self.validated_data['username']
        )

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords dont match'})
        
        account.set_password(pw)
        account.save()
        return account
    

class LoginTokenSerializer(serializers.Serializer):

    """
    Serializer to validate user credentials and authenticate by username and password.
    Adds authenticated user to validated data or raises validation error on failure.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, payload):

        """
        Authenticates the user using username and password.
        Adds the authenticated user to the validated payload or raises an error on failure.
        """
        payload_username = payload.get('username')
        payload_password = payload.get('password')

        try:
            user = User.objects.get(email=payload_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username or password is not correct")

        user = authenticate(username=payload_username, password=payload_password)
        if not user:
            raise serializers.ValidationError("Username or password is not correct")

        payload['user'] = user
        return payload