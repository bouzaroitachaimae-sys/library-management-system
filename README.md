# library-management-system
Django web app for library management with book catalog, reservations, user authentication and admin panel.

## Features
- Book catalog with category filtering and search
- Book reservation and rental system
- User authentication (register, login, logout)
- User profile with reservation history
- Admin panel for managing books and categories
- Book availability tracking in real time
- Cover image upload support

## Technologies Used
- Python
- Django 4.2+
- SQLite
- Pillow (image handling)
- HTML / CSS Templates

## Project Structure
bibliotheque/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── bibliotheque/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── livres/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── reservations/
├── models.py
├── views.py
└── urls.py

## Installation
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Apply migrations:
   python manage.py migrate
4. Create admin user:
   python manage.py createsuperuser
5. Run the server:
   python manage.py runserver

## Pages
- **Accueil** - Home with recent books
- **Livres** - Full catalog with search and filters
- **Réservations** - Book reservation management
- **Profil** - User profile and history
- **Admin** - /admin for administrators

## Localization
- Language: French
- Timezone: Africa/Casablanca
