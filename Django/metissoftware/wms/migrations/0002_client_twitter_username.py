# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='twitter_username',
            field=models.CharField(null=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Not a valid username,please remove @ and max of 15 cahracters', regex='^(\\w){1,15}$')]),
            preserve_default=True,
        ),
    ]
