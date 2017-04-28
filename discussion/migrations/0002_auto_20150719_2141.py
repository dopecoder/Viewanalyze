# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(unique=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tertiary_tag',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
