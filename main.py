import os
import django


# Set the default settings module for the Django environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Vendor_Management_System_with_Performance_Metrices.settings")
# Initialize Django

django.setup()

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from myapp.controller import vendor_router, vendor_performance, purchase_router

# Create a new FastAPI instance
app = FastAPI()


app.include_router(vendor_router,prefix='/api/vendors',tags=["Vendors Profile Management"])
app.include_router(purchase_router,prefix='/api/purchase_orders',tags=["Purchase Order Tracking"])
app.include_router(vendor_performance,prefix='/api/vendors/<int:vendor_id>/performance',tags=["Vendor Performance Evaluation"])



@app.get('/')
def root():
    return {"msg":"hi"}
