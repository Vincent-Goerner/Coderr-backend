# Coderr Offer Management System

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
