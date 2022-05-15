# Django-Rest Demo Project

The app provides web api to create and link users with car models into a persistant db. 

The projects uses Django, Django Rest Framework, Django Filters and Yet another Swagger generator


1. Installation

- Use requirements.txt

- Replace templates in venv\Lib\site-packages
- app links:
* /admin
* /accounts/signup
* accounts/login
* accounts/logout
* /api
* /swagger


2. Usage

- manage.py runserver

- We have admin interface
http://127.0.0.1:8000/admin/
U:1 P:1

- And regular user interface
http://127.0.0.1:8000/

- You can run reload_test_data.py to start with fresh lists for brands and models

3. To do

- fix post requests for CarModel and UserCar
- improve urls
