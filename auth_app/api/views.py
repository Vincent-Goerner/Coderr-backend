from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotFound, PermissionDenied
from .serializers import RegistrationSerializer, LoginTokenSerializer, UserProfileSerializer
from auth_app.models import UserProfile


class RegistrationView(APIView):
    """
    APIView to handle user registration by validating input and creating a new user.
    Returns auth token and user info on success, or 400 error with validation details.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validates registration data, creates a new user, and returns a token with user info.
        Returns 400 with error details if validation fails.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
        else:
            return Response({'400': 'Ungültige Anfragedaten.', 'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data)
    

class CustomLoginView(ObtainAuthToken):
    """
    APIView to authenticate users by email and password, returning an auth token and user info.
    Handles validation errors with detailed 400 responses.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticates user via email and password, and returns token with user info.
        Returns 400 with error message if authentication fails.
        """
        serializer = LoginTokenSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
        else:
            return Response({'400': 'Ungültige Anfragedaten.', 'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data)
    

class ProfileDetailView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        user_id = self.kwargs.get('pk')

        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("No user profile found")
        except Exception as e:
            raise PermissionDenied(f"Fehler: {str(e)}")

        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user.id != profile.user.id:
                raise PermissionDenied("You are not allowed to edit a other profile then yours.")
            
        return profile
    

class BusinessProfileListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request):
        business_profiles = UserProfile.objects.filter(type="business")
        serializer = UserProfileSerializer(business_profiles, many=True)
        return Response(serializer.data)  
    

class CustomerProfileListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request):
        customer_profiles = UserProfile.objects.filter(type="customer")
        serializer = UserProfileSerializer(customer_profiles, many=True)
        return Response(serializer.data)  