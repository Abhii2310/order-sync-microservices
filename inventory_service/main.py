from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import SessionLocal, engine, Base
import models
import schemas


import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="Inventory Service")

@app.on_event("startup")
async def register_to_eureka():
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="inventory-service",
        instance_port=8002,
    )

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # in prod you restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/inventory/{product_id}", response_model=schemas.InventoryOut)
def get_inventory(product_id: str, db: Session = Depends(get_db)):
    record = (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == product_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    return record


@app.post("/api/inventory", response_model=schemas.InventoryOut, status_code=201)
def create_or_update_inventory(
    item: schemas.InventoryCreate, db: Session = Depends(get_db)
):
    record = (
        db.query(models.Inventory)
        .filter(models.Inventory.product_id == item.product_id)
        .first()
    )

    if record:
        record.quantity = item.quantity
    else:
        record = models.Inventory(
            product_id=item.product_id, quantity=item.quantity
        )
        db.add(record)

    db.commit()
    db.refresh(record)
    return record


@app.get("/api/inventory", response_model=List[schemas.InventoryOut])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(models.Inventory).all()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "inventory"}
