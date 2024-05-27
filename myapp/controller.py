from http.client import HTTPException
from typing import List

from datetime import datetime
from fastapi import APIRouter
from .models import Vendor, PurchaseOrder
from .schema import VendorOut, VendorIn, PurchaseOrderOut, PurchaseOrderIn
from .logic import (
    calculate_on_time_delivery_rate,
    calculate_quality_rating_avg,
    calculate_average_response_time,
    calculate_fulfillment_rate,
    update_vendor_performance_metrics
)

vendor_router = APIRouter()
purchase_router = APIRouter()
vendor_performance = APIRouter()


# Vendor Endpoints
@vendor_router.get("/api/vendors/", response_model=List[VendorOut])
def read_vendors():
    vendors = Vendor.objects.all()
    return list(vendors)


@vendor_router.post("/api/vendors/", response_model=VendorOut)
def create_vendor(vendor: VendorIn):
    vendor_obj = Vendor(**vendor.dict())
    vendor_obj.save()
    return vendor_obj


@vendor_router.get("/api/vendors/{vendor_id}/", response_model=VendorOut)
def get_vendor(vendor_id: int):
    vendor = Vendor.objects.filter(id=vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@vendor_router.put("/api/vendors/{vendor_id}/", response_model=VendorOut)
def update_vendor(vendor_id: int, vendor: VendorIn):
    vendor_obj = Vendor.objects.filter(id=vendor_id).first()
    if not vendor_obj:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for field, value in vendor.dict().items():
        setattr(vendor_obj, field, value)
    vendor_obj.save()
    return vendor_obj


@vendor_router.delete("/api/vendors/{vendor_id}/")
def delete_vendor(vendor_id: int):
    vendor_obj = Vendor.objects.filter(id=vendor_id).first()
    if not vendor_obj:
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor_obj.delete()
    return {"detail": "Vendor deleted successfully"}


# Vendor Performance Endpoint
@vendor_performance.get("/api/vendors/{vendor_id}/performance")
def get_vendor_performance(vendor_id: int):
    vendor = Vendor.objects.filter(id=vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor_id)
    quality_rating_avg = calculate_quality_rating_avg(vendor_id)
    average_response_time = calculate_average_response_time(vendor_id)
    fulfillment_rate = calculate_fulfillment_rate(vendor_id)

    return {
        "vendor_id": vendor_id,
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_rating_avg": quality_rating_avg,
        "average_response_time": average_response_time,
        "fulfillment_rate": fulfillment_rate
    }


# Purchase Order Endpoints
@purchase_router.get("/api/purchase_orders/", response_model=List[PurchaseOrderOut])
def read_purchase_orders(vendor_id: int = None):
    if vendor_id:
        purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
    else:
        purchase_orders = PurchaseOrder.objects.all()
    return list(purchase_orders)


@purchase_router.post("/api/purchase_orders/", response_model=PurchaseOrderOut)
def create_purchase_order(po: PurchaseOrderIn):
    po_obj = PurchaseOrder(**po.dict())
    po_obj.save()
    update_vendor_performance_metrics(po_obj.vendor_id)  # Update metrics after creating a PO
    return po_obj


@purchase_router.get("/api/purchase_orders/{po_id}/", response_model=PurchaseOrderOut)
def get_purchase_order(po_id: int):
    po = PurchaseOrder.objects.filter(id=po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po


@purchase_router.put("/api/purchase_orders/{po_id}/", response_model=PurchaseOrderOut)
def update_purchase_order(po_id: int, po: PurchaseOrderIn):
    po_obj = PurchaseOrder.objects.filter(id=po_id).first()
    if not po_obj:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    for field, value in po.dict().items():
        setattr(po_obj, field, value)
    po_obj.save()
    update_vendor_performance_metrics(po_obj.vendor_id)  # Update metrics after updating a PO
    return po_obj


@purchase_router.delete("/api/purchase_orders/{po_id}/")
def delete_purchase_order(po_id: int):
    po_obj = PurchaseOrder.objects.filter(id=po_id).first()
    if not po_obj:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    vendor_id = po_obj.vendor_id
    po_obj.delete()
    update_vendor_performance_metrics(vendor_id)  # Update metrics after deleting a PO
    return {"detail": "Purchase Order deleted successfully"}


# New endpoint for acknowledging a purchase order
@purchase_router.post("/api/purchase_orders/{po_id}/acknowledge")
def acknowledge_purchase_order(po_id: int):
    po = PurchaseOrder.objects.filter(id=po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    po.acknowledgment_date = datetime.now()
    po.save()
    update_vendor_performance_metrics(po.vendor_id)  # Recalculate average response time

    return {"detail": "Purchase order acknowledged successfully"}
