from django.db import models
import itertools
from django.utils.text import slugify


# Create your models here.

TECH = ((0, 'Inner Sphere'), (1, 'Clan'), (2, 'Prototype'))
ROLE = ((0, 'Ambusher'), (1, 'Brawler'), (2, 'Juggernaut'), (3, 'Missle Boat'), (4, 'Scout'), (5, "Skirmisher"), (6, 'Sniper'), (7, 'Striker'))
CLASSIFICATION = ((0, 'Light'), (1, 'Medium'), (2, 'Heavy'), (3, 'Assault'))
WEIGHTS = ((0, '20 Ton'), (1, '25 Ton'), (2, '30 Ton'), (3, '35 Ton'), (4, '40 Ton'), (5, '45 Ton'), (6, '50 Ton'), (7, '55 Ton'), (8, '60 Ton'), (9, '65 Ton'), (10, '70 Ton'), (11, '75 Ton'), (12, '80 Ton'), (13, '85 Ton'), (14, '90 Ton'), (15, '95 Ton'), (16, '100 Ton'))
STATUS = ((0, "Not Available"), (1, "Available"))

   
class Mech(models.Model):

    name = models.CharField(max_length=50, unique=True)
    category = models.IntegerField(choices=CLASSIFICATION, default=0)
    weight = models.IntegerField(choices=WEIGHTS, default=0)
    tech_level = models.IntegerField(choices=TECH, default=0)
    role = models.IntegerField(choices=ROLE, default=0)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    record_sheet = models.CharField(max_length=50, default='custom')
    battle_value = models.IntegerField(default=9999)
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name