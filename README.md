# Expense Tracker

A modern full-stack Expense Tracker web application built using Django and Tailwind CSS.  
It allows users to manage their expenses, visualize spending patterns, and track financial activity through an intuitive dashboard.

---

## Features

- User Authentication (Login / Signup / Logout)
- Add Expenses
- Dashboard with Total Spending
- Doughnut Chart (Category-wise spending using Chart.js)
- Monthly Bar-Chart
- Filtering Expenses
- Budget Alerts
- Delete Expenses
- User-specific data (each user sees only their expenses)
- Modern UI with Tailwind CSS (Glassmorphism Design)
- Fully Responsive

---

## Tech Stack

- Backend: Django (Python)
- Frontend: HTML, Tailwind CSS
- Database: SQLite (default)
- Charts: Chart.js

---

## ⚙️ Installation (macOS)

### 1. Clone the Repository
git clone https://github.com/your-username/expense-tracker.git  
cd expense-tracker

### 2. Create Virtual Environment
python3 -m venv venv  
source venv/bin/activate  

### 3. Install Dependencies
pip install django  

### 4. Run Migrations
python manage.py makemigrations  
python manage.py migrate  

### 5. Create Superuser
python manage.py createsuperuser  

### 6. Run Server
python manage.py runserver  

Visit: http://127.0.0.1:8000/

---

## Project Structure

expense_tracker/  
│── tracker/  
│   ├── models.py  
│   ├── views.py  
│   ├── forms.py  
│   ├── urls.py  
│  
│── templates/  
│   ├── base.html  
│   ├── login.html  
│   ├── signup.html  
│   ├── dashboard.html  
│   ├── add_expense.html  
│  
│── manage.py  

---

## Delete a User (Shell)

python manage.py shell  

from django.contrib.auth.models import User  
User.objects.get(username="your_username").delete()  

---

## Future Enhancements

- Edit Expenses    
- Export to CSV/PDF  

---

## Author

Pranav Kumar
Safin Joash Xavier
Gargi Pant

---
