# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0002_client_twitter_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('startDateTime', models.DateTimeField()),
                ('endDateTime', models.DateTimeField()),
                ('type', models.CharField(default='meeting', max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('fa', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(upload_to='client_images', default='/media/person-placeholder.png'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fa',
            name='image',
            field=models.ImageField(upload_to='fa_images', default='/media/person-placeholder.png'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='twitter_username',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Not a valid username,please remove @ and max of 15 cahracters', regex='^(\\w){1,15}$')], blank=True, max_length=15),
            preserve_default=True,
        ),
    ]
