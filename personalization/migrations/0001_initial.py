# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0021_auto_20150812_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitedTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Analyser', models.OneToOneField(to='discussion.Analyser')),
                ('category', models.ManyToManyField(to='discussion.Category')),
                ('secondaryTag', models.ManyToManyField(to='discussion.SecondaryTag')),
                ('tertiaryTag', models.ManyToManyField(to='discussion.TertiaryTag')),
            ],
        ),
    ]
