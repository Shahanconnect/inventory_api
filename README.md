# 📦 Inventory Management API (Async - FastAPI)

Hi, I'm Shahan, and this is my **Inventory Management API** built using **FastAPI**, **SQLAlchemy 2.x async**, and **Alembic**.  
It’s a clean, modular, and lightweight backend designed to manage products and stock transactions efficiently — perfect for small business or warehouse inventory use cases.

---

## 🚀 Features

- 📄 Create, update, delete, and view products
- 🔄 Record stock IN / OUT transactions
- 📦 Track inventory quantity in real-time
- 🧠 Clean async architecture using SQLAlchemy 2.x
- 🎯 Built with FastAPI + SQLite + Alembic

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Shahanconnect/inventory_api.git
cd inventory_api

python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload

## 📸 Screenshots

## Screenshot Preview


## API Screenshots

### Product List – JSON
![Product JSON](https://raw.githubusercontent.com/Shahanconnect/inventory_api/main/api_screenshots/product-list-jason.PNG)

### Product List – Table
![Product Table](https://raw.githubusercontent.com/Shahanconnect/inventory_api/main/api_screenshots/product-list-table.PNG)


