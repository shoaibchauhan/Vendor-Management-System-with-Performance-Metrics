from datetime import datetime
from django.db.models import Avg, Sum, F
from .models import PurchaseOrder, Vendor, HistoricalPerformance


def calculate_on_time_delivery_rate(vendor_id):
    total_completed_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed').count()
    on_time_pos = PurchaseOrder.objects.filter(
        vendor_id=vendor_id, status='completed', delivery_date__gte=F('order_date')
    ).count()
    if total_completed_pos == 0:
        return 0
    return on_time_pos / total_completed_pos


def calculate_quality_rating_avg(vendor_id):
    avg_quality_rating = \
    PurchaseOrder.objects.filter(vendor_id=vendor_id, status='completed').aggregate(Avg('quality_rating'))[
        'quality_rating__avg']
    return avg_quality_rating if avg_quality_rating is not None else 0


def calculate_average_response_time(vendor_id):
    pos = PurchaseOrder.objects.filter(vendor_id=vendor_id, acknowledgment_date__isnull=False)
    total_response_time = pos.aggregate(total_response_time=Sum(
        F('acknowledgment_date') - F('issue_date')
    ))['total_response_time']
    if total_response_time is None or pos.count() == 0:
        return 0
    return total_response_time.total_seconds() / pos.count() / 3600  # convert seconds to hours


def calculate_fulfillment_rate(vendor_id):
    total_pos = PurchaseOrder.objects.filter(vendor_id=vendor_id).count()
    fulfilled_pos = PurchaseOrder.objects.filter(
        vendor_id=vendor_id, status='completed', quality_rating__isnull=False
    ).count()
    if total_pos == 0:
        return 0
    return fulfilled_pos / total_pos


def update_vendor_performance_metrics(vendor_id):
    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor_id)
    quality_rating_avg = calculate_quality_rating_avg(vendor_id)
    average_response_time = calculate_average_response_time(vendor_id)
    fulfillment_rate = calculate_fulfillment_rate(vendor_id)

    vendor = Vendor.objects.get(id=vendor_id)
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    # Update historical performance
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=datetime.now(),
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate
    )
