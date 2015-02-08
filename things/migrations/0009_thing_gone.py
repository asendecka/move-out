# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0008_taker_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='gone',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
