from rest_framework import serializers
from orders.models import Order
from offers.models import OfferDetails


class OrderSerializer(serializers.ModelSerializer):
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
    offer_detail_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ["offer_detail_id"]

    def create(self, validated_data):
        offer_detail_id = validated_data.pop("offer_detail_id")
        offer_detail = OfferDetails.objects.get(id=offer_detail_id)
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
        return OrderSerializer(instance, context=self.context).data