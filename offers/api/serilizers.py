from django.contrib.auth.models import User
from rest_framework import serializers
from offers.models import Offer, OfferDetails


class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

    def get_details(self, obj):
        return [
            {
                "id": detail.id,
                "title": detail.title,
                "revisions": detail.revisions,
                "delivery_time_in_days": detail.delivery_time_in_days,
                "price": detail.price,
                "features": detail.features or [],
                "offer_type": detail.offer_type,
                "url": f"/offerdetails/{detail.id}/" 
            }
            for detail in obj.details.all()
        ]


    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user  

        details_data = self.initial_data.get("details", [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)

        return offer

    def validate(self, data):
        details = self.initial_data.get("details", None)
        method = self.context.get("request").method if self.context.get("request") else None

        if method == "POST" or "PATCH":
            if not details or len(details) != 3:
                raise serializers.ValidationError({
                    "non_field_errors": ["Exactly three details (basic, standard, premium) are required."]
                })
            offer_types = [d["offer_type"] for d in details]
            if len(set(offer_types)) != 3 or not all(typ in ["basic", "standard", "premium"] for typ in offer_types):
                raise serializers.ValidationError({
                    "non_field_errors": ["Details must include exactly one of each: basic, standard, premium."]
                })

        return data

    def update(self, instance, validated_data):
        details_data = self.initial_data.get("details", None)
        offer = super().update(instance, validated_data)

        if details_data is not None:
            offer.details.all().delete()
            for detail_data in details_data:
                detail_data.pop('offer', None)
                OfferDetails.objects.create(offer=offer, **detail_data)

        return offer
    
class OfferDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OfferDetails
        fields = '__all__'
    
    def validate(self, data):
        errors = self._validate_fields(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def _validate_fields(self, data):
        revisions = data.get('revisions')
        delivery_time_in_days = data.get('delivery_time_in_days')
        features = data.get('features')
        price = data.get('price')
        errors = {}
        if revisions is not None and revisions < 0:
            errors["revisions"] = ["Revisions numbers are not allowed to be lower than 0."]
        if delivery_time_in_days is not None and delivery_time_in_days <= 0:
            errors["delivery_time_in_days"] = ["Delivery tim must be more than 1 day."]
        if not features or len(features) == 0:
            errors["features"] = ["The minimum of one feature need to be set."]
        if price is not None and price <= 0:
            errors["price"] = ["Price must be higher than 1."]
        return errors
        