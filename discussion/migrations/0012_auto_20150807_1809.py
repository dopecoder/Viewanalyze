# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0011_auto_20150805_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='ter_tag',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='personalization',
            name='TertiaryTag',
            field=models.ManyToManyField(to='discussion.TertiaryTag'),
        ),
        migrations.AddField(
            model_name='personalization',
            name='primaryCategory',
            field=models.ManyToManyField(to='discussion.Category'),
        ),
        migrations.AddField(
            model_name='personalization',
            name='secondaryCategory',
            field=models.ManyToManyField(to='discussion.SecondaryTag'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='open_status',
            field=models.CharField(default=b'OPEN', max_length=6, choices=[(b'OPEN', b'discussion open'), (b'CLOSED', b'discussion closed')]),
        ),
    ]
