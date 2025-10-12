from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration handling full name parsing and password validation.
    Ensures email uniqueness and matching passwords before creating a new user.
    """
    username = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
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
            raise serializers.ValidationError('Email already exists.')
        return value
    
    def create(self, validated_data):

        validated_data.pop('repeated_password')
        user_type = validated_data.pop('type', None)

        if not user_type:
            raise serializers.ValidationError("User type is requiered.")

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)

        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user, type=user_type)
        else:
            print(f"UserProfile für {user.username} existiert bereits.")
        
        return user
    

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
            user = User.objects.get(username=payload_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Username or password is not correct")

        user = authenticate(username=payload_username, password=payload_password)
        if not user:
            raise serializers.ValidationError("Username or password is not correct")

        payload['user'] = user
        return payload
    

class UserProfileSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        )
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user.save()
        instance.save()
        return instance