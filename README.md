# Vendor Booking API - Phase 1

API-first backend for a vendor booking platform. Built with FastAPI.

## Features

- Users, Vendors, and Bookings management
- RESTful CRUD API
- Auto-generated OpenAPI documentation
- In-memory datastore (for now)

## Tech Stack

- FastAPI (Python)
- Docker
- Terraform (AWS EKS, ECR, IAM)
- Helm (K8s)
- GitHub Actions (CI/CD)
- Prometheus + Grafana + Fluent Bit (Monitoring/Logging)

## Run Locally

```bash
uvicorn app.main:app --reload
