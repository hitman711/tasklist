# Task List DRF with user permission

An Example Django REST framework project for filter data from DB with some API restriction.

## API Swagger View

* **/swagger/doc/**		(Swagger document view)
* **rest/swagger/doc/**		(Rest swagger view)


## API Endpoints

* **/task/list/**	(Task List end point)
* **/task/{task_id}/**  (Task Reatrieve, Update and delete endpoint)
* **/registration/** (User registration API endpoint)
* **/sign-in/**		(User sign in API endpoint)

* Filters also available on above API endpoints

## Requirements

* **python==3.*
* **Django==1.11.13
* **djangorestframework-filters==0.10.2
* **djangorestframework==3.6.4
* **psycopg2==2.7.3.1
* **pytz==2017.2


## Installation

* Create global environment for project

    mkvirtualenv <env_name> (virtualenv)

* Clone project repository in your system and move inside project folder
* Activate virtualenv and install project requirements

    pip install -r requirements.txt

* Run migrations first before loading fixtures

    python manage.py migrate

* Load fixtures data (**Note** :- Only for testing purpose, No need to load on production server)

    python manage.py loaddata fixtures/*

* Create SuperUser incase want to se django default admin panel

    python manage.py createsuperuser

* Run test cases to check all created functionality is working in all scenario

    python manage.py test


# Default View
Default page contain dashboard which show total record of Questions, Answers, Users and Tenant. Also show total API hit made by tenant