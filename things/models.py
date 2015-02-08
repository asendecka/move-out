from uuid import uuid4
import os

from django.conf import settings
from django.db import models


def get_image_path(instance, filename):
    filename = os.path.basename(filename)
    return os.path.join('things/pictures', str(uuid4())[:8], filename)


class Taker(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=100, default=uuid4, unique=True)
    email = models.EmailField(null=True, blank=True)
    email_sent = models.DateTimeField(null=True, editable=False)

    def taken_things(self):
        return Thing.objects.filter(taken_by=self)

    def __unicode__(self):
        return self.name


class Thing(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=get_image_path, blank=True)
    taken_by = models.ForeignKey(Taker, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gone = models.BooleanField(default=False)

    def give_to(self, taker):
        if self.taken_by:
            raise ValueError("Cannot give the same thing twice")
        self.taken_by = taker
        self.save()

    def give_back(self, taker):
        if self.taken_by == taker:
            self.taken_by = None
            self.save()

    def is_gone(self):
        self.gone = True
        self.save()

    def is_not_gone(self):
        self.gone = False
        self.save()

    @property
    def picture_url(self):
        return settings.MEDIA_URL + self.picture.name

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    things = models.ManyToManyField(Thing)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
