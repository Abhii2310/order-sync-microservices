from fastapi import FastAPI, HTTPException
from typing import List
from bson import ObjectId

from db import products_collection
from schemas import ProductCreate, ProductOut
import py_eureka_client.eureka_client as eureka_client

import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="Product Service")

@app.on_event("startup")
async def register_to_eureka():
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="product-service",
        instance_port=8001,
    )




def product_to_out(doc) -> ProductOut:
    return ProductOut(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc.get("description"),
        price=doc["price"],
    )


@app.post("/api/products", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate):
    doc = product.dict()
    result = products_collection.insert_one(doc)
    created = products_collection.find_one({"_id": result.inserted_id})
    return product_to_out(created)


@app.get("/api/products", response_model=List[ProductOut])
def list_products():
    docs = list(products_collection.find())
    return [product_to_out(d) for d in docs]


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "product"}
