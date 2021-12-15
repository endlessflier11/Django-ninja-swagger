from django.test import TestCase
from rest_framework.test import APIClient
from django import urls
from character_api.tests.factories.user import UserFactory
from character_api.tests.factories.character import RoleFactory, CharacterFactory
from character_api.models import Role


class TestRoleApi(TestCase):
    URL = urls.reverse("api-1.0.0:character_role")

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_not_logged_in_401_get(self):
        response = self.client.get(self.URL, format='json')
        self.assertEqual(response.status_code, 401)

    def test_not_logged_in_401_post(self):
        response = self.client.post(
            self.URL, {"label": "hero"}, format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_role_get_404_not_there(self):
        self.client.force_login(self.user)
        response = self.client.get(
            urls.reverse("api-1.0.0:character_role", args=[1])
        )
        self.assertEqual(response.status_code, 404)

    def test_character_role_get(self):
        self.client.force_login(self.user)
        role = RoleFactory.create(id=1, label="new-label")
        response = self.client.get(
            urls.reverse("api-1.0.0:character_role", args=[1])
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["id"], role.id)
        self.assertEqual((json["label"]), role.label)

    def test_get(self):
        self.client.force_login(self.user)
        RoleFactory.create_batch(n_roles_in_db := 5)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json), n_roles_in_db)
        all_have_labels = len([j for j in json if "label" in j]) == n_roles_in_db
        self.assertTrue(all_have_labels)

    def test_post(self):
        self.client.force_login(self.user)
        data = {"label": "hero"}
        response = self.client.post(
            self.URL, data, format='json'
        )

        self.assertEqual(response.status_code, 200)
        json = response.json()

        self.assertEqual(json["label"], data["label"])
        self.assertTrue("id" in json)

        entity_created = Role.objects.filter(id=json["id"]).first() is not None
        self.assertTrue(
             entity_created
        )


# Test for character api
class TestCharacterApi(TestCase):
    URL = urls.reverse("api-1.0.0:character_list")

    def setUp(self):
        """ set up test client and user """
        self.client = APIClient() # test client
        self.user = UserFactory() # test client for character api
    
    def test_not_logged_in_401_get(self):
        """ test to get characters list when user is not logged in """
        response = self.client.get(self.URL, format='json') # call the character list api
        self.assertEqual(response.status_code, 401) # check if status code equals 401 or not
    
    def test_character_list_get(self):
        """ test to get characters list when user is logged in """
        self.client.force_login(self.user) # login user
        CharacterFactory.create_batch(n_roles_in_db := 10) # create 10 characters instance
        response = self.client.get(
            urls.reverse("api-1.0.0:character_list") # call the character list api
        )
        self.assertEqual(response.status_code, 200) # check if status code equals 200 or not
        json = response.json()
        self.assertEqual(len(json), n_roles_in_db) # check if length of json equals 10 or not
        all_have_names = len([j for j in json if "name" in j]) == n_roles_in_db 
        self.assertTrue(all_have_names) # check if all characters have name or not

    def test_character_list_get_with_role(self):
        """ test to get filtered chatacters list by passing role query params """
        self.client.force_login(self.user) # login user
        role = RoleFactory.create(id=1, label="new-label") # create role instance
        CharacterFactory.create_batch(n_roles_in_db := 10, role=role) # create 10 characters instance with role
        response = self.client.get(
            urls.reverse("api-1.0.0:character_list"), # call the character list api
            {"role": 1}
        )
        self.assertEqual(response.status_code, 200) # check if status code equals 200 or not
        json = response.json()
        self.assertEqual(len(json), n_roles_in_db) # check if length of json equals 10 or not
        all_have_names = len([j for j in json if "name" in j]) == n_roles_in_db
        self.assertTrue(all_have_names) # check if all characters have name or not
        self.assertEqual(json[0]["role"]["id"], role.id) # check if role id of first character equals role id or not
        self.assertEqual(json[0]["role"]["label"], role.label) # check if role label of first character equals role label or not

    def test_character_put(self):
        """ test to update character values using put method """
        self.client.force_login(self.user) # login user
        character = CharacterFactory.create(id=1, name="new-name") # create character instance
        response = self.client.put(
            urls.reverse("api-1.0.0:character_update", args=[1]), # call the character update api
            {"name": "new-name-updated"},
            format='json'
        )
        self.assertEqual(response.status_code, 200) #   check if status code equals 200 or not
        json = response.json()
        self.assertEqual(json["id"], character.id)
        self.assertEqual((json["name"]), "new-name-updated") #  check if name of character equals updated name or not
        