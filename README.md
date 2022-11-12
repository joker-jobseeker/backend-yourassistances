Getting started.

Overviews
This repository contains work of back-end of YourAssistance.

This project is built with React that generated using Vite as its build tool and use Python as Flask Framework.

Installation
make sure your python is installed: https://www.python.org/

install venv:
python -m venv venv
activate: 
source venv/Scripts/activate # windows
source venv/bin/activate # mac or linux

install required package: 
pip install -r requirements.txt

how to running this project:
export FLASK_APP=main.py
export FLASK_ENV=development
flask db init
flask db upgrade
flask run

License
The MIT License (MIT). Please see License File for more information.

Credits
Name	Profile
Muhammad Hafid Kurnianton	hafidkrntn
Muhammad Ihsan Abdurrohman	mohehsan