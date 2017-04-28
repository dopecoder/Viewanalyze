# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import viewanalyse.path


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Analyser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('country', models.CharField(max_length=40)),
                ('dob', models.DateField()),
                ('total_upvotes', models.IntegerField(default=0, blank=True)),
                ('no_discussions', models.IntegerField(default=0, blank=True)),
                ('no_replied', models.IntegerField(default=0, blank=True)),
                ('reputation', models.IntegerField(default=0, blank=True)),
                ('achievements', models.ManyToManyField(to='discussion.Achievement')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_attachments', models.ImageField(null=True, upload_to=viewanalyse.path.image_upload_path_generic, blank=True)),
                ('document_attachments', models.FileField(null=True, upload_to=viewanalyse.path.document_upload_path_generic, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_attachments', models.ImageField(null=True, upload_to=viewanalyse.path.avatar_upload_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image_attachments', models.ImageField(null=True, upload_to=viewanalyse.path.image_upload_path, blank=True)),
                ('document_attachments', models.FileField(null=True, upload_to=viewanalyse.path.document_upload_path, blank=True)),
                ('upvotes', models.IntegerField(default=0, null=True, blank=True)),
                ('views', models.IntegerField(default=0, null=True, blank=True)),
                ('replies', models.IntegerField(default=0, null=True, blank=True)),
                ('no_replies', models.IntegerField(default=0, null=True, blank=True)),
                ('open_status', models.CharField(default=b'OPEN', max_length=6, choices=[(b'OPEN', b'deiscussion open'), (b'CLOSED', b'discussion closed')])),
                ('privacy_status', models.CharField(default=b'PUBLIC', max_length=7, choices=[(b'PUBLIC', b'public discussion'), (b'PRIVATE', b'private discussion')])),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('weightage', models.IntegerField(default=0, null=True, blank=True)),
                ('analyser', models.ForeignKey(to='discussion.Analyser', null=True)),
                ('category', models.ForeignKey(to='discussion.Category', null=True)),
                ('discussion_followers', models.ManyToManyField(related_name='analyser_followers', to='discussion.Analyser')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='DiscussionTimeLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('discussion', models.OneToOneField(to='discussion.Discussion')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Discussor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('upvotes', models.IntegerField(default=0, blank=True)),
                ('context', models.CharField(max_length=50, null=True)),
                ('no_reply_followers', models.IntegerField(default=0, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('analyser', models.ForeignKey(to='discussion.Analyser', null=True)),
                ('attachments', models.OneToOneField(null=True, blank=True, to='discussion.Attachment')),
                ('discussion', models.ForeignKey(to='discussion.Discussion')),
                ('reply_followers', models.ManyToManyField(related_name='reply_followers', to='discussion.Analyser')),
                ('reply_to', models.ForeignKey(blank=True, to='discussion.DiscussionTimeLine', null=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Personalization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secondary_tag', models.CharField(max_length=100)),
                ('tertiary_tag', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='discussion.Category')),
            ],
        ),
        migrations.AddField(
            model_name='discussor',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='tags',
            field=models.ManyToManyField(to='discussion.Tag'),
        ),
        migrations.AddField(
            model_name='analyser',
            name='avatar',
            field=models.OneToOneField(null=True, blank=True, to='discussion.Avatar'),
        ),
        migrations.AddField(
            model_name='analyser',
            name='discussions_following',
            field=models.ManyToManyField(related_name='discussions_following_rel_+', to='discussion.Analyser'),
        ),
        migrations.AddField(
            model_name='analyser',
            name='followers',
            field=models.ManyToManyField(related_name='users_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='analyser',
            name='following',
            field=models.ManyToManyField(related_name='users_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='analyser',
            name='personalization',
            field=models.OneToOneField(null=True, blank=True, to='discussion.Personalization'),
        ),
        migrations.AddField(
            model_name='analyser',
            name='replys_following',
            field=models.ManyToManyField(related_name='replys_following_rel_+', to='discussion.Analyser'),
        ),
        migrations.AddField(
            model_name='analyser',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
