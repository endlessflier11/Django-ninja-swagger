from typing import List
from django.shortcuts import get_object_or_404
from django.urls.base import resolve
from ninja import Router
from character_api import models
from character_api.schemas import CharacterOut, CharacterIn
from ninja.security import django_auth


character_router = Router()

# Api to get list of all characters
@character_router.get(
    '/', # path of the api
    response=List[CharacterOut], # response schema of the api
    auth=django_auth, # To check if user is authenticated or not
    url_name="character_list", # url name of the api
    tags=["Character"], # tags of the api
)
def get_characters(request,role: str = None):
    """Fetch the list of characters, you can even filter the characters by passing the role params in the query parameters"""
    characters = models.Character.objects.all() # Fetch all the characters
    if(role): # Checking if role is passed in query params, if passed then filter the characters by role
        # getting instance of the role using string
        role_instance = models.Role.objects.filter(label=role)
        # if role params is valid
        if(len(role_instance)):
            # Filter the characters by role
            characters = characters.filter(role=role_instance[0])
    return characters

# API to update any field of a character
@character_router.put(
    '/{int:character_id}', # path of the api, chatacter_id is the primary key of the character
    response=CharacterOut, # response schema of the api
    auth=django_auth, # To check if user is authenticated or not
    url_name="character_update", # url name of the api
    tags=["CharacterUpdate"] # tags of the api
)
def update_character(request,character_id:int,payload:CharacterIn):
    """character_id is the id of character instance to be updated"""
    character = get_object_or_404(models.Character,id=character_id) # getting the character instance, return 404 if character not found
    for attr, value in payload.dict().items(): # iterating over the payload, payload is the data sent by the user
        # attr is the name of field and value is the value of that field
        if value:
            if(attr == 'role'):
                # getting instance of the role using label
                character.role = get_object_or_404(models.Role,label=value)
            else:
                # setting the value of the field
                setattr(character, attr, value)
    character.save() # save the character instance
    return character