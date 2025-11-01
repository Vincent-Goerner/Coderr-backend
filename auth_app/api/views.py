from django.db.models import Avg
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotFound, PermissionDenied
from .serializers import RegistrationSerializer, LoginTokenSerializer, UserProfileSerializer, BusinessProfilesSerializer, CustomerProfilesSerializer
from auth_app.models import UserProfile
from reviews.models import Review
from offers.models import Offer


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
    """
    API view to retrieve or update a user's profile.
    Allows only authenticated users and restricts edits to the profile owner.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieves the requested user profile and checks edit permissions.
        Raises errors if the profile doesn't exist or the user isn't the owner.
        """
        user_id = self.kwargs.get('pk')

        try:
            profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("No user profile found")
        except Exception as e:
            raise PermissionDenied(f"Fehler: {str(e)}")

        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user.id != profile.user.id:
                raise PermissionDenied("Only the owner can edit a profile.")
            
        return profile
    

class BaseInfoView(APIView):
    """
    Public API view returning basic platform statistics.
    Provides counts for reviews, business profiles, offers, and the average rating.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns general platform statistics including reviews, ratings, 
        business profiles, and offers for public access.
        """
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0
        business_profile_count = UserProfile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        
        return Response(data) 
    

class BusinessProfileListView(APIView):
    """
    API view for authenticated users to retrieve all business profiles.
    Returns serialized data for profiles of type 'business'.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request):
        """
        Retrieves and returns all business-type user profiles 
        as serialized data for authenticated users.
        """
        business_profiles = UserProfile.objects.filter(type="business")
        serializer = BusinessProfilesSerializer(business_profiles, many=True)
        return Response(serializer.data)  
    

class CustomerProfileListView(APIView):
    """
    API view for authenticated users to retrieve all customer profiles.
    Returns serialized data for profiles of type 'customer'.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request):
        """
        Retrieves and returns all customer-type user profiles 
        as serialized data for authenticated users.
        """
        customer_profiles = UserProfile.objects.filter(type="customer")
        serializer = CustomerProfilesSerializer(customer_profiles, many=True)
        return Response(serializer.data)  