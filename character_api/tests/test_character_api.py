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


class TestCharacterApi(TestCase):
    URL = urls.reverse("api-1.0.0:character_list")

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
    
    def test_not_logged_in_401_get(self):
        response = self.client.get(self.URL, format='json')
        self.assertEqual(response.status_code, 401)
    
    # test to get characters list
    def test_character_list_get(self):
        self.client.force_login(self.user)
        CharacterFactory.create_batch(n_roles_in_db := 10)
        response = self.client.get(
            urls.reverse("api-1.0.0:character_list")
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json), n_roles_in_db)
        all_have_names = len([j for j in json if "name" in j]) == n_roles_in_db
        self.assertTrue(all_have_names)
    
    # test to get characters by passing role query params
    def test_character_list_get_with_role(self):
        self.client.force_login(self.user)
        role = RoleFactory.create(id=1, label="new-label")
        CharacterFactory.create_batch(n_roles_in_db := 10, role=role)
        response = self.client.get(
            urls.reverse("api-1.0.0:character_list"),
            {"role": 1}
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(len(json), n_roles_in_db)
        all_have_names = len([j for j in json if "name" in j]) == n_roles_in_db
        self.assertTrue(all_have_names)
        self.assertEqual(json[0]["role"]["id"], role.id)
        self.assertEqual(json[0]["role"]["label"], role.label)
    
    # test to update character values using put method
    def test_character_put(self):
        self.client.force_login(self.user)
        character = CharacterFactory.create(id=1, name="new-name")
        response = self.client.put(
            urls.reverse("api-1.0.0:character_update", args=[1]),
            {"name": "new-name-updated"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["id"], character.id)
        self.assertEqual((json["name"]), "new-name-updated")
        