# 🍕 Pizza Delivery Backend API

This is a backend RESTful API for a Pizza Delivery application built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**.

## 🚀 Features

- User Registration & Login with JWT Authentication
- Role-based Access Control (Admin / User)
- Place Orders
- Database Integration using SQLAlchemy ORM
- Input Validation using Pydantic
- Clean and Modular Code Structure

## 🛠️ Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication

## 🗂️ Project Structure

FastAPI Project/
│
├── main.py # FastAPI application entry
├── models.py # Database models
├── schemas.py # Pydantic models (request/response)
├── database.py # DB connection setup
├── auth_routes.py # User auth (login/register)
├── order_routes.py # Order management routes
├── init_db.py # DB table initialization
├── requirements.txt # Python dependencies


## 📦 Setup Instructions

git clone https://github.com/lokesh-git-ctrl/Pizza-Delivery-BackEnd-API-Project.git
cd Pizza-Delivery-BackEnd-API-Project

python -m venv venv
venv\Scripts\activate   # On Windows

pip install -r requirements.txt

uvicorn main:app --reload

Then open in browser: http://127.0.0.1:8000/docs

📌 API Documentation:
  FastAPI provides Swagger UI automatically. You can access it at:
  
👉 Swagger Docs: http://127.0.0.1:8000/docs

👤 Author
Lokesh
GitHub: lokesh-git-ctrl
