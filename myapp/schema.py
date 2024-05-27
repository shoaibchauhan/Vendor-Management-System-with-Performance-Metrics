from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# Vendor Schemas
class VendorIn(BaseModel):
    name: str = Field(..., max_length=255)
    contact_details: str
    address: str
    vendor_code: str = Field(..., max_length=100)
    on_time_delivery_rate: Optional[float] = None
    quality_rating_avg: Optional[float] = None
    average_response_time: Optional[float] = None
    fulfillment_rate: Optional[float] = None

class VendorOut(VendorIn):
    id: int

# Purchase Order Schemas
class PurchaseOrderIn(BaseModel):
    po_number: str = Field(..., max_length=100)
    vendor_id: int
    order_date: datetime
    delivery_date: datetime
    items: Dict[str, Any]
    quantity: int
    status: str = Field(..., max_length=50)
    quality_rating: Optional[float] = None
    issue_date: datetime
    acknowledgment_date: Optional[datetime] = None

class PurchaseOrderOut(PurchaseOrderIn):
    id: int

# Historical Performance Schemas
class HistoricalPerformanceIn(BaseModel):
    vendor_id: int
    date: datetime
    on_time_delivery_rate: float
    quality_rating_avg: float
    average_response_time: float
    fulfillment_rate: float

class HistoricalPerformanceOut(HistoricalPerformanceIn):
    id: int
