OrderSync – Microservices Order Management System

OrderSync is a distributed microservices-based Order Management System built using FastAPI, MongoDB, MySQL, Eureka Discovery & API Gateway architecture.
It enables users to create products, update inventory, place orders, and track activities through a responsive web UI.

Frontend (UI)
      ↓
API Gateway (FastAPI)
      ↓
 
 │            Eureka            │
 │     Service Discovery        │
 
      ↓            ↓             ↓
Product Service  Inventory Service  Order Service
 (MongoDB)          (MySQL)           (MySQL)

>How Eureka Helps

Without Eureka:
Gateway uses hard-coded URLs → Not scalable

With Eureka:
Each microservice registers dynamically
Gateway auto-discovers service locations
Enables load balancing & auto healing

If a service restarts or scales up, Eureka automatically updates its location.

Folder Structure
order-sync-microservices
│
├── gateway/                # API Gateway (FastAPI)
├── product_service/        # MongoDB Product Microservice
├── inventory_service/      # MySQL Inventory Microservice
├── order_service/          # MySQL Order Microservice
├── eureka-server/          # Spring Boot Eureka Server
├── ui/                     # Web UI Dashboard
├── docker-compose.yml      # (optional for future deployment)
├── README.md               # Project documentation
└── .gitignore
