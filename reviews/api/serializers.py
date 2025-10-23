from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'business_user', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        
        reviewer = self.context['request'].user
        if not reviewer.is_authenticated:
            raise serializers.ValidationError({"detail": ["You need to be authenticated to create a review."]})
        if 'reviewer' in self.initial_data and int(self.initial_data['reviewer']) != reviewer.id:
            raise serializers.ValidationError({"detail": ["You cannot create a review on behalf of another user."]})
        business_user = data.get('business_user')
        if self.instance is None and Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError({"detail": ["You can only give one review per profile."]})
        return data
    
    def create(self, validated_data):
        
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)