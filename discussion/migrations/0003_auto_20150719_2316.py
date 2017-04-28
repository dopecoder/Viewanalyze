# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0002_auto_20150719_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow_category', models.CharField(max_length=11)),
            ],
        ),
        migrations.RenameField(
            model_name='achievement',
            old_name='name',
            new_name='achievement',
        ),
        migrations.RemoveField(
            model_name='analyser',
            name='achievements',
        ),
        migrations.RemoveField(
            model_name='analyser',
            name='discussions_following',
        ),
        migrations.RemoveField(
            model_name='analyser',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='analyser',
            name='following',
        ),
        migrations.RemoveField(
            model_name='analyser',
            name='replys_following',
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='discussion_followers',
        ),
        migrations.RemoveField(
            model_name='discussor',
            name='reply_followers',
        ),
        migrations.AddField(
            model_name='achievement',
            name='analyser',
            field=models.ForeignKey(to='discussion.Analyser', null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='analyser',
            field=models.ForeignKey(blank=True, to='discussion.Analyser', null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='discussion',
            field=models.ForeignKey(blank=True, to='discussion.Discussion', null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='followed_by', to='discussion.Analyser'),
        ),
        migrations.AddField(
            model_name='follow',
            name='reply',
            field=models.ForeignKey(blank=True, to='discussion.Discussor', null=True),
        ),
    ]
