import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import SessionLocal, engine, Base
import models
import schemas


import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="Order Service")

@app.on_event("startup")
async def register_to_eureka():
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="order-service",
        instance_port=8003,
    )


Base.metadata.create_all(bind=engine)

INVENTORY_SERVICE_URL = os.getenv(
    "INVENTORY_SERVICE_URL", "http://localhost:8002"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/orders", response_model=schemas.OrderOut, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Call Inventory Service to check stock
    try:
        resp = httpx.get(
            f"{INVENTORY_SERVICE_URL}/api/inventory/{order_in.product_id}",
            timeout=5.0,
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503, detail="Inventory service unavailable"
        )

    if resp.status_code == 404:
        raise HTTPException(
            status_code=400, detail="Product not found in inventory"
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Error from inventory service"
        )

    data = resp.json()
    available_qty = data.get("quantity", 0)

    if available_qty < order_in.quantity:
        raise HTTPException(
            status_code=400, detail="Not enough stock available"
        )

    order = models.Order(
        product_id=order_in.product_id,
        quantity=order_in.quantity,
        status="CREATED",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@app.get("/api/orders", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "order"}
