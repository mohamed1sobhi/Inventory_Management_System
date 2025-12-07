# Inventory Management System

## Project Overview
The Inventory Management System is a web-based platform designed to manage product inventory for a warehouse supplying supermarkets. It provides functionality for tracking shipments from factories, managing orders from supermarkets, and overseeing product stock. The system includes role-based access, ensuring that only authorized personnel can perform critical operations.

## Presentaion
[Inventory Management System](https://drive.google.com/file/d/1Lh9vmqMSr14Fa0Ly2nC48cIKTYMk0b8-/view?usp=sharing)


## Tech Stack
- **Backend:** Django, Python
- **Frontend:** HTML, CSS, JavaScript , Bootstrap5 , Jquery
- **Database:** PostgreSQL
- **Authentication:** Django's built-in authentication system

## Features
- **User Authentication:** Role-based access control with Manager and Employee roles.
- **Product Management:** Add, update, and monitor product stock, with alerts for critical inventory levels.
- **Order Management:** Create, approve, and track orders placed by supermarkets.
- **Shipment Management:** Record shipments from factories, approve them, and track incoming stock.
- **Role-Based Access:** Managers can approve orders/shipments, while employees can only create them.
- **Dashboard:** Overview of inventory, pending approvals, and recent activity (for managers only).

## Database Models
The system consists of four main models:
- **User:** Custom user model with roles (Manager/Employee).
- **Product:** Tracks product details and stock levels.
- **Order:** Records supermarket orders, including status and approver.
- **Shipment:** Tracks incoming shipments from factories.

## ERD
[Models](https://drive.google.com/file/d/1HwJKbcEZubhvWgMqRJcqynJo6tz8HGyY/view?usp=drive_link)

## Team Members
- **Ahmed Mazen** - Project Leader
- **Attia Elkhamy**
- **Rashida Shokr**
- **Mohamed Sobhi**
- **Islam Zaki**

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-repo/inventory-management-system.git
```
2. Navigate into the project directory:
```bash
cd inventory-management-system
```
3. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Apply migrations:
```bash
python manage.py migrate
```
6. Run the server:
```bash
python manage.py runserver
```
7. Access the app at `http://127.0.0.1:8000/`

## Usage
- Log in with your credentials.
- Navigate through the dashboard to manage products, orders, and shipments.
- Approve pending orders/shipments if you have the Manager role.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```
3. Commit changes:
```bash
git commit -m "Add: Your feature description"
```
4. Push your branch:
```bash
git push origin feature/your-feature-name
```
5. Create a Pull Request.
