from django.db.models import QuerySet

class OrderingHelperOffers:
    ORDERING_OPTIONS = {
        "-updated_at": "-updated_at",
        "updated_at": "updated_at",
        "-min_price": "-min_price",
        "min_price": "min_price",
    }

    @staticmethod
    def apply_ordering(queryset: QuerySet, ordering: str) -> QuerySet:
        ordering_field = OrderingHelperOffers.ORDERING_OPTIONS.get(ordering, "-created_at")
        return queryset.order_by(ordering_field)