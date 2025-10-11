from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from .serializers import ProfileDetailSerializer
from django.contrib.auth.models import User


class ProfileDetailView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        user_id = self.kwargs.get('pk')

        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            raise NotFound("No user profile found")
        
        return profile