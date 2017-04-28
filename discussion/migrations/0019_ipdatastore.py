# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0018_discussioncontentupdate_discussionupdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpDataStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipAddr', models.CharField(max_length=16)),
                ('views', models.CharField(max_length=2000, null=True, blank=True)),
            ],
        ),
    ]
