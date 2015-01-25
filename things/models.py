from uuid import uuid4

from django.db import models


class Taker(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=100, default=uuid4, unique=True)

    def __unicode__(self):
        return self.name


class Thing(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="things/pictures/", blank=True)
    taken_by = models.ForeignKey(Taker, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def give_to(self, taker):
        if self.taken_by:
            raise ValueError("Cannot give the same thing twice")
        self.taken_by = taker
        self.save()

    def give_back(self, taker):
        if self.taken_by == taker:
            self.taken_by = None
            self.save()

    def __unicode__(self):
        return self.name
