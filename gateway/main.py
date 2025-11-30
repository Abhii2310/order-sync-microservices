import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="API Gateway")

@app.on_event("startup")
async def register_to_eureka():
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="api-gateway",
        instance_port=9000,
    )

# --- CORS so browser can call http://localhost:9000 from file / Live Server ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # for demo; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL", "http://localhost:8002")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8003")


async def proxy_request(request: Request, base_url: str, path_suffix: str = "") -> Response:
    """
    Generic reverse proxy that forwards method, headers, body, and query params
    to a target microservice.

    Special case: for CORS preflight (OPTIONS) we answer directly from gateway
    with 200 so that backend services don't need OPTIONS routes.
    """
    # CORS preflight: don't forward, just OK
    if request.method == "OPTIONS":
        return Response(status_code=200)

    url = f"{base_url}{path_suffix}"
    method = request.method
    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()
    params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method,
            url,
            content=body,
            headers=headers,
            params=params,
        )

    excluded_headers = {"content-length", "transfer-encoding", "connection"}
    response_headers = {
        k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers
    }

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}


# ---------- Products ----------
@app.api_route("/api/products", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def products_proxy(request: Request, path: str = ""):
    suffix = "/api/products" + (f"/{path}" if path else "")
    return await proxy_request(request, PRODUCT_SERVICE_URL, suffix)


# ---------- Inventory ----------
@app.api_route("/api/inventory", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/inventory/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def inventory_proxy(request: Request, path: str = ""):
    suffix = "/api/inventory" + (f"/{path}" if path else "")
    return await proxy_request(request, INVENTORY_SERVICE_URL, suffix)


# ---------- Orders ----------
@app.api_route("/api/orders", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def orders_proxy(request: Request, path: str = ""):
    suffix = "/api/orders" + (f"/{path}" if path else "")
    return await proxy_request(request, ORDER_SERVICE_URL, suffix)
