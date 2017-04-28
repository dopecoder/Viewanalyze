# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0016_discussionupvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]
