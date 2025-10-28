# Coderr

## 🔍 Overview
Coderr is a Django-based Offer Management System developed as part of the Developer Akademie program. It allows registered users to create offers, place orders, manage profiles, and leave reviews. The system supports pagination, filtering, secure authentication, and a clean API structure.

## ✨ Features

### Sales Page
- Displays all published offers

### Login & Registration
- Token-based authentication with user profile assignment (Customer/Business)

### Offer Management
- Create, list, update, and delete offers
- Nested OfferDetails for multiple packages (basic, standard, premium)

### User Profiles
- Manage Business and Customer profiles
- Update own profile data
- List view of all business or customer profiles

### Orders
- Customers can place orders based on offers
- Business users can update order status (e.g., "in progress", "completed")

### Reviews
- Customers can rate business users
- Full CRUD with access control

### Legal Pages
- Privacy Policy & Imprint pages

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- SQLite (default) or PostgreSQL for production
- Virtual environment recommended (venv or pipenv)

### Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/Vincent-Goerner/Coderr-Backend.git
cd coderr-backend

# 2. Create virtual environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file (see .env.example)

# 5. Run migrations
python manage.py migrate

# 6. Start development server
python manage.py runserver
```

## 🚀 API Endpoints (Examples)

### ✍️ Offers
| Method | Endpoint                | Description                                       |
| ------ | ----------------------- | ------------------------------------------------- |
| GET    | /api/offers/            | List all offers (supports filtering & pagination) |
| POST   | /api/offers/            | Create a new offer                                |
| GET    | /api/offers/{id}/       | Retrieve a single offer                           |
| PATCH  | /api/offers/{id}/       | Update offer (only owner)                         |
| DELETE | /api/offers/{id}/       | Delete offer (only owner)                         |
| GET    | /api/offerdetails/{id}/ | Retrieve specific offer detail                    |


### 📦 Orders
| Method | Endpoint          | Description                              |
| ------ | ----------------- | ---------------------------------------- |
| GET    | /api/orders/      | View your orders                         |
| POST   | /api/orders/      | Place a new order                        |
| PATCH  | /api/orders/{id}/ | Update order status (only business user) |


### ⭐ Reviews
| Method | Endpoint           | Description   |
| ------ | ------------------ | ------------- |
| GET    | /api/reviews/      | List reviews  |
| POST   | /api/reviews/      | Create review |
| PATCH  | /api/reviews/{id}/ | Update review |
| DELETE | /api/reviews/{id}/ | Delete review |


### 👤 Profiles
Method	Endpoint	Description
| Method | Endpoint                | Description                |
| ------ | ----------------------- | -------------------------- |
| GET    | /api/profile/{id}/      | View profile               |
| PATCH  | /api/profile/{id}/      | Update profile             |
| GET    | /api/profiles/business/ | List all business profiles |
| GET    | /api/profiles/customer/ | List all customer profiles |


### 🔐 Authentication
| Method | Endpoint           |
| ------ | ------------------ |
| POST   | /api/login/        |
| POST   | /api/registration/ |


### 📊 Miscellaneous
| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| GET    | /api/base-info/ | General platform statistics |



## 🔧 Development Standards

Clean Code: Methods < 14 lines

Naming: snake_case for functions and variables

No dead/commented-out code

PEP-8 Compliance: All Python files follow PEP-8 guidelines

## 🚫 Security & .env

This project uses a .env file to manage environment-specific and sensitive settings such as:

SECRET_KEY

DEBUG

Database paths and other credentials

The .env file is excluded from version control (.gitignore), but a .env.template is provided as a template.
Please copy .env.template to .env and fill in your own values before running the project.

## 📄 License

Open-source project for educational purposes. Not intended for commercial use.
