Hungry Burger
An online burger ordering web application built with Django. Customers can browse the menu, customize items, place orders for pickup, and track their order status. Administrators manage the menu, orders, and promotions through Django's admin panel.
Built for ELE3921 Web Application Development, Spring 2026, BI Norwegian Business School.

Quick Setup 
Enter the commands below step-by-step in the terminal,
Terminal shortcut: ctrl+` 
(the key in the top left corner!)

1/ Load in the repo
git clone https://github.com/ShockZeRa1/Hungry-Burger.git
cd Hungry-Burger
python -m venv .venv

2/ Activate the virtual environment:
Windows: .\.venv\Scripts\Activate.ps1
Mac/Linux: source .venv/bin/activate

3/ Then install, migrate, and load sample data:
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata data_dump.json
python manage.py runserver


Test Credentials:
user: yousuf
pass: 123qwerty


A sample discount code BURGER10 (10% off) is included and can be applied at checkout.

The site runs at http://127.0.0.1:8000 and the admin panel at http://127.0.0.1:8000/admin


Key Functions:
As a customer (http://127.0.0.1:8000):

The homepage displays the full menu with a featured items section at the top
Click any product to see its detail page with customization options (extra patties, sauces, etc.)
Add items to cart, you will also see a floating cart icon in the bottom-right which updates in real time
Open the cart to adjust quantities or remove items
At checkout, apply the discount code BURGER10 and add a customer note
Guest checkout is available without creating an account
Log in as yousuf to see past orders and use the re-order button

As an administrator (http://127.0.0.1:8000/admin):

Products: Create, edit, and delete menu items with images and pricing
Categories: Organize the menu (Meal Deals, Burgers, Fries, Drinks, Dips)
Option Groups & Options: Manage product customizations and their prices
Orders: View all placed orders with customer details and item breakdowns
Order Statuses: Update an order through its lifecycle (Order Placed -> Preparing -> Ready for Pickup -> Picked Up)
Discount Codes: Create promotional codes with percentage or fixed discounts, expiry dates, and usage limits

Tech Stack
Django 6.0.2, Python 3.12.6, django-allauth, django-jazzmin, Bootstrap 5, SQLite.

More information in project report.