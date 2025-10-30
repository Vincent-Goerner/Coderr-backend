from rest_framework import serializers
from offers.models import Offer, OfferDetails


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the Offer model including nested OfferDetails.
    Handles creation, update, and validation of exactly three details (basic, standard, premium).
    Provides read-only aggregated fields like min_price and min_delivery_time.
    """
    min_price = serializers.FloatField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = serializers.SerializerMethodField()
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        read_only_fields = ['user']

    def get_details(self, obj):
        """
        Returns a serialized list of related OfferDetails for the given Offer.
        """
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
        """
        Creates an Offer and its nested OfferDetails, linking the current user automatically.
        """
        request = self.context.get("request")
        validated_data["user"] = request.user  

        details_data = self.initial_data.get("details", [])
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)

        return offer

    def validate(self, data):
        """
        Ensures exactly three details are provided: basic, standard, and premium.
        Raises ValidationError if the requirements are not met.
        """
        details = self.initial_data.get("details", None)
        method = self.context.get("request").method if self.context.get("request") else None

        if method == "POST":
            if not details or len(details) != 3:
                raise serializers.ValidationError({
                    "non_field_errors": ["Exactly three details (basic, standard, premium) are required."]
                })
            offer_types = [d["offer_type"] for d in details]
            if len(set(offer_types)) != 3 or not all(typ in ["basic", "standard", "premium"] for typ in offer_types):
                raise serializers.ValidationError({
                    "non_field_errors": ["Details must include exactly one of each: basic, standard, premium."]
                })
            
        if method == "PATCH":
            if details:
                for detail in details:
                    if "offer_type" not in detail:
                        raise serializers.ValidationError({
                            "details": {"offer_type": ["Dieses Feld ist erforderlich."]}
                        })

        return data

    def update(self, instance, validated_data):
        """
        Updates an Offer and partially updates its nested OfferDetails if provided.
        """
        details_data = self.initial_data.get("details", None)
        offer = super().update(instance, validated_data)

        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                if not offer_type:
                    continue

                detail_obj = offer.details.filter(offer_type=offer_type).first()
                if detail_obj:
                    for field, value in detail_data.items():
                        if field not in ["id", "offer_type", "offer"]:
                            setattr(detail_obj, field, value)
                    detail_obj.save()
                else:
                    detail_data.pop("offer", None)
                    OfferDetails.objects.create(offer=offer, **detail_data)

        return offer
    
    
class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfferDetails model.
    Handles validation for revisions, delivery time, features, and price fields.
    Ensures all fields meet business rules before saving.
    """    
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
    
    def validate(self, data):
        """
        Validates OfferDetails fields and raises a ValidationError if any constraints are violated.
        """
        errors = self._validate_fields(data)
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def _validate_fields(self, data):
        """
        Performs field-level checks:
        - revisions must be >= 0
        - delivery_time_in_days must be > 0
        - at least one feature is required
        - price must be > 0
        Returns a dictionary of errors if present.
        """
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
        