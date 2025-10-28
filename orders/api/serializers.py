from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from orders.models import Order
from offers.models import OfferDetails


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model, handling conversion between Order instances and JSON,
    including all relevant fields such as customer, business, title, price, status, and timestamps.
    """
    price = serializers.FloatField()
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",    
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Orders from an OfferDetail ID, validates revisions,
    assigns customer and business users, and returns the created Order via OrderSerializer.
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ["offer_detail_id"]

    def create(self, validated_data):
        """
        Creates a new Order from a provided offer_detail_id, validates revisions,
        assigns customer and business users, and sets order fields based on the OfferDetails.
        """
        offer_detail_id = validated_data.pop("offer_detail_id")
        offer_detail = get_object_or_404(OfferDetails, id=offer_detail_id)
        offer = offer_detail.offer
        request = self.context.get("request")
        customer_user = request.user
        business_user = offer.user

        revisions = offer_detail.revisions
        if revisions != -1 and revisions < 1:
            raise serializers.ValidationError({"revisions": "Revisions can't be lower than 1."})

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress"
        )
        return order

    def to_representation(self, instance):
        """
        Returns the serialized representation of the Order instance using OrderSerializer,
        ensuring consistent output format for API responses.
        """
        return OrderSerializer(instance, context=self.context).data
    
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Orders; only allows the 'status' field to be modified,
    and raises a ValidationError if any other fields are included in the update.
    """
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]

    def update(self, instance, validated_data):
        """
        Updates an Order instance, allowing only the 'status' field to be modified.
        Raises a ValidationError if any other fields are included in the update.
        """
        allowed_fields = {"status"}
        invalid_fields = set(validated_data.keys()) - allowed_fields

        if invalid_fields:
            raise ValidationError(f"Only 'status' can be updated. Invalid fields: {', '.join(invalid_fields)}")

        return super().update(instance, validated_data)