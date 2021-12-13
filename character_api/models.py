
from django.db import models


class Role(models.Model):
    label = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = True
        db_table = 'role'


class Alignment(models.TextChoices):
     lg="Lawful Good"
     ng="Neutral Good"
     cg="Chaotic Good"
     ln="Lawful Neutral"
     nn="Neutral"
     cn="Chaotic Neutral"
     le="Lawful Evil"
     ne="Neutral Evil"


class Character(models.Model):
    name = models.CharField(unique=True, max_length=255)
    role = models.ForeignKey(Role, null=True, on_delete=models.DO_NOTHING)
    alignment = models.CharField(
        choices=Alignment.choices, null=True, max_length=100, blank=True
    )

    class Meta:
        managed = True
        db_table = 'character'
