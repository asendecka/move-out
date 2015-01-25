# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0002_auto_20150124_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(default=uuid.uuid4, unique=True,
                                           max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='thing',
            name='taken_by',
            field=models.ForeignKey(blank=True, to='things.Taker', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ThingTaker',
        ),
    ]
