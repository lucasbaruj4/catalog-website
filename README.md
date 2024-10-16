# 📦 Catalog Website

This repository contains both the **frontend** and **backend** of a catalog web application. The frontend is built using **Quasar** (Vue.js) and JavaScript, while the backend is developed using **Flask** with **SQLAlchemy** for database management.

## 📁 Project Structure

- `catalogo-frontend/`: This folder contains all the source code related to the frontend of the application.
- `catalogo-backend/`: This folder contains all the source code related to the backend of the application.

### Technologies used:

- **Frontend**: 
  - Quasar Framework (Vue.js)
  - HTML, CSS, JavaScript
- **Backend**:
  - Flask
  - SQLAlchemy (for database management)
  - Python


## ⚙️ Project Setup

### Frontend

1. Navigate to the frontend directory:
cd catalogo-frontend
2. Install the dependencies:
npm install
3. Run the development server:
quasar dev
4. Build for production:
quasar build

### Backend 
1. Navigate to the backend directory:
cd catalogo-backend
2. Create a virtual environment (optional, but recommended):
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
3. Install the dependencies:
pip install -r requirements.txt
4. Run the Flask server:
flask run

### 🛠 Features
**Frontend**: Users can browse the catalog, search for products, and view product details.
**Backend**: The server handles CRUD operations (create, read, update, delete) for products and categories in the catalog.
