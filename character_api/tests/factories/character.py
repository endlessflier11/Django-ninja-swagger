from character_api.models import Role,Character,Alignment
import factory

 
class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    label = factory.Sequence(lambda n: 'label-%s' % n)


# Factory for Character Model
class CharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character
    
    name = factory.Sequence(lambda n: 'name-%s' % n) # fake name of character, Exampel: name-1, name-2, name-3
    role = factory.SubFactory(RoleFactory) # fake role of character
    alignment = factory.Faker('random_choices',elements=Alignment.choices) # fake alignment of character, the alignment will be chosen randomly from Alignment.choices