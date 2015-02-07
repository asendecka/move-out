# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0007_auto_20150207_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='taker',
            name='email_sent',
            field=models.DateTimeField(null=True, editable=False),
            preserve_default=True,
        ),
    ]
