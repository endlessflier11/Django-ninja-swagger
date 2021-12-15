from typing import List
from django.shortcuts import get_object_or_404
from django.urls.base import resolve
from ninja import Router
from character_api import models
from character_api.schemas import CharacterOut, CharacterIn
from ninja.security import django_auth


character_router = Router()


@character_router.get(
    '/',
    response=List[CharacterOut],
    auth=django_auth,
    url_name="character_list",
    tags=["Character"],
)
def get_characters(request,role: str = None):
    """Fetch the list of characters, you can even filter the characters by passing the  role params in the query parameters"""
    characters = models.Character.objects.all()
    # Checking if role is passed in query params
    if(role):
        # getting instance of the role using string
        role_instance = models.Role.objects.filter(label=role)
        # if role params is valid
        if(len(role_instance)):
            characters = characters.filter(role=role_instance[0])
    return characters


@character_router.put(
    '/{int:character_id}',
    response=CharacterOut,
    auth=django_auth,
    url_name="character_update",
    tags=["CharacterUpdate"]
)
def update_character(request,character_id:int,payload:CharacterIn):
    """character_id is the id of character instance to be updated"""
    character = get_object_or_404(models.Character,id=character_id)
    for attr, value in payload.dict().items():
        if value:
            if(attr == 'role'):
                character.role = get_object_or_404(models.Role,label=value)
            else:
                setattr(character, attr, value)
    character.save()
    return character