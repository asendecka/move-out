from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class ThingTaker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    token = models.CharField(max_length=100, default=uuid4, unique=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.first_name, self.last_name)


class Thing(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="things/pictures/", blank=True)
    taken_by = models.ForeignKey(ThingTaker, null=True, blank=True)

    def give_to(self, taker):
        self.taken_by = taker
        self.save()

    def give_back(self, taker):
        if self.taken_by == taker:
            self.taken_by = None
            self.save()

    def __unicode__(self):
        return self.name
