# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0007_auto_20150731_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateDiscussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analyser', models.ManyToManyField(to='discussion.Analyser')),
                ('discussion', models.ForeignKey(to='discussion.Discussion')),
            ],
        ),
    ]
