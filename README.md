# django + django ninja + factory boy + pipenv setup
An example django RESTapi setup.

### Installation
You'll need python3.8 and pipenv installed to get going.

```bash
git clone https://github.com/mrJeppard/django_ninja_factoryboy_pipenv.git

cd django_ninja_factoryboy_pipenv && pipenv install
```

### Run the server and interact with the swagger docs
```pipenv run python manage.py makemigrations```

```pipenv run python manage.py migrate```

```pipenv run python manage.py create_user test@test.com password```

```pipenv run python manage.py runserver```

Login via [localhost:8000/accounts/login](localhost:8000/accounts/login)

### Run the tests
`pipenv run python manage.py test`



