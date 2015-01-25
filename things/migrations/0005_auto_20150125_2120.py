# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import things.models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0004_thing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='picture',
            field=models.ImageField(upload_to=things.models.get_image_path, blank=True),
            preserve_default=True,
        ),
    ]
