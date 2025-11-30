OrderSync – Microservices Order Management System

OrderSync is a full microservices-based Order Management System developed using modern distributed architecture.
The system allows a business to manage products, update inventory, and process orders — exactly like real e-commerce platforms such as Amazon / Flipkart.

This project demonstrates API Gateway + Microservices + Service Discovery with a responsive Web UI.

<>Why Eureka is Used (Simple Explanation)

Without Eureka ❌
Every microservice URL must be hard-coded in the gateway (example: localhost:8001).
If any service restarts or changes its port → system fails.

With Eureka ✔
Each service automatically registers itself in Eureka with its IP & port
API Gateway asks Eureka where a service is running
Even if a service restarts / scales / moves to another machine → system continues smoothly

➡️ This makes the project scalable, fault-tolerant and production-ready.
