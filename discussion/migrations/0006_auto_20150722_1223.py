# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0005_auto_20150721_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondaryTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secondary_tag', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='discussion.Category')),
            ],
        ),
        migrations.CreateModel(
            name='TertiaryTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tertiary_tag', models.CharField(max_length=100)),
                ('secondary_tag', models.ForeignKey(to='discussion.SecondaryTag')),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='category',
        ),
        migrations.RemoveField(
            model_name='discussion',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='discussor',
            name='tags',
        ),
        migrations.AlterField(
            model_name='discussor',
            name='slug',
            field=models.SlugField(max_length=1000, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='discussion',
            name='secondary_tag',
            field=models.ManyToManyField(to='discussion.SecondaryTag'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='tertiary_tag',
            field=models.ManyToManyField(to='discussion.TertiaryTag'),
        ),
        migrations.AddField(
            model_name='discussor',
            name='secondary_tag',
            field=models.ManyToManyField(to='discussion.SecondaryTag'),
        ),
        migrations.AddField(
            model_name='discussor',
            name='tertiary_tag',
            field=models.ManyToManyField(to='discussion.TertiaryTag'),
        ),
    ]
