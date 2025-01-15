Nocta E-Commerce Website
This project is an e-commerce platform developed using Django. It provides a platform where users can browse and purchase products, sellers can manage their products, and content can inform users.


Features:

Product listing and detail pages
Posts and content management
Admin panel for content and user management
Static file handling and media uploads


Requirements:

To run the project, you need the following software installed:

Python 3.9 or newer
Django 4.x
SQLite (used by default)
Virtual environment (virtualenv or venv)


Installation
1.Clone the repository:

--bash--
git clone <project-repo-url>
cd nocta


2.Create and activate a virtual environment:

--bash--
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate


3.Install dependencies:

--bash--
pip install -r requirements.txt


4.Set up the database:

--bash--
python manage.py migrate


5.Collect static files:

--bash--
python manage.py collectstatic


6.Start the server:

--bash--
python manage.py runserver

Open http://127.0.0.1:8000 or localhost:8000 in your browser to view the project.


Admin Panel
To access the admin panel, create a superuser:

--bash--
python manage.py createsuperuser

After logging in, access the panel at http://127.0.0.1:8000/admin. (or localhost:8000)

Project Structure
blog/: Modules for the application
core/: Core application
static/: Static files (CSS, JS, images)
templates/: HTML templates
media/: User-uploaded files
db.sqlite3: SQLite database file
manage.py: Django management tool