# Stores REST API

This is built with Flask, Flask-RESTful, Flask-JWT, Flask-JWT-Extended and Flask-SQLAlchemy (ORM).

Deployed on Heroku and DigitalOcean.

### Usage:

Clone the repository:
```sh
git clone https://github.com/noameron/REST-API.git 
```
Install requirements:
```sh
virtualenv venv --python=python3
pip install -r requirements.txt
```

Start the REST-API:
```sh
./main.py
```

### Usage Examples:
- using [HTTPie]

Get all available items:
```sh
http http://localhost:5000/items
```

Add an item:
```sh
http post http://localhost:5000/item/apple price=1 store_id=1
```

Register a new user:
```sh
http post http://localhost:5000/register username="omri" password="abc"
```

Authenticate a user:
```sh
http post http://localhost:5000/auth username="omri" password="abc"
```


[HTTPie]: <https://httpie.io>
