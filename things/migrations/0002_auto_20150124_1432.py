# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThingTaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, blank=True)),
                ('token', models.CharField(default=uuid.uuid4, max_length=100,
                                           editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='thing',
            name='taken_by',
            field=models.ForeignKey(blank=True, to='things.ThingTaker',
                                    null=True),
            preserve_default=True,
        ),
    ]
