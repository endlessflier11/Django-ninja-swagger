from character_api.models import Role
import factory


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    label = factory.Sequence(lambda n: 'label-%s' % n)
