# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0015_discussion_analyser_upvoted'),
    ]

    operations = [
        migrations.CreateModel(
            name='discussionUpvote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analyser', models.ForeignKey(to='discussion.Analyser')),
                ('discussion', models.ForeignKey(to='discussion.Discussion')),
            ],
        ),
    ]
