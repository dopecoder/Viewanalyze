# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0022_discussion_isfrompublic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_type', models.CharField(max_length=6, choices=[(b'FGU', b'Following updates'), (b'FRU', b'followers updates'), (b'DU', b'Discussion updates'), (b'SU', b'System updates'), (b'INVITE', b'Invite notification')])),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isUpdated', models.BooleanField(default=False)),
                ('analyser', models.OneToOneField(to='discussion.Analyser')),
                ('nofications', models.ManyToManyField(to='discussion.Notification')),
            ],
        ),
        migrations.AlterField(
            model_name='follow',
            name='follow_category',
            field=models.CharField(max_length=11, choices=[(b'ANALYSER', b'analyser'), (b'REPLY', b'reply'), (b'DISCUSSION', b'discussion')]),
        ),
    ]
