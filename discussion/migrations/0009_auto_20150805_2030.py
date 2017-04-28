# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0008_privatediscussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussionReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analyser', models.ForeignKey(blank=True, to='discussion.Analyser', null=True)),
                ('discussion', models.ForeignKey(to='discussion.Discussion')),
            ],
        ),
        migrations.RemoveField(
            model_name='tertiarytag',
            name='secondary_tag',
        ),
    ]
