# MyAcademy
[![Build Status](https://travis-ci.org/kiarashgl/MyAcademy.svg?branch=master)](https://travis-ci.org/kiarashgl/MyAcademy)

Website for comparing universities, departments and professors.

Systems Analysis and Design course project, developed using Scrum methodology.

## About
This website is used to get information about quality of teaching and academic services in different universities, and choose the right one.
Also, it has a blog to discuss about different topics in academic fields.

## Wiki
For more information, please read the [Wiki](https://github.com/kiarashgl/MyAcademy/wiki) page.

## Run
To run this project, first clone it. Then, create a python virtual environment and activate it.
```bash
virtualenv venv
source venv/bin/activate
```
After that, install the requirements with `pip install -r requirements.txt`. Then migrate the database with
```bash
python manage.py migrate
```
Also, you could compile the translations using
```bash
python manage.py compilemessages
```
At last, run the server:
```bash
python manage.py runserver
```

## Requirements
- Python 3.8+
- Django 3+
- A computer with a web browser
