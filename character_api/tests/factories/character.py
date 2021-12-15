from character_api.models import Role,Character,Alignment
import factory

 
class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    label = factory.Sequence(lambda n: 'label-%s' % n)


class CharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character
    
    name = factory.Sequence(lambda n: 'name-%s' % n)
    role = factory.SubFactory(RoleFactory)
    alignment = factory.Faker('random_choices',elements=Alignment.choices)