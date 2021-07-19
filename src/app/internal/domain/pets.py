from django.db import models
from datetime import datetime

class Pet(models.Model):
    name = models.CharField(max_length=255)
    birthdate = models.DateField()

    def __str__(self):
        return self.name

    @property
    def age(self):
        return 42