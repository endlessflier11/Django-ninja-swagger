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



## Gilbish Kosma's work
1) Creation of character_api file
   - In character_api.py i have created the following api:
     - Api to get the list of characters, user can also filter characters by role,
     - Api to update the fields of a character.

2) creation of Factory for Character model in tests/factories.py
   - In tests/factories.py i have created the following factory:
     - CharacterFactory

3) Writing tests for the Character API
   - In tests/test_character_api.py i have created the following tests:
     - test_get_characters_list
     - test_get_characters_list_with_role
     - test_update_character