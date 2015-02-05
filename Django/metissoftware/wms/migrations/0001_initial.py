# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FA',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=64)),
                ('first_name', models.CharField(default='**DEFAULT**', max_length=64)),
                ('surname', models.CharField(default='**DEFAULT**', max_length=64)),
                ('dob', models.DateField(default='1990-01-01')),
                ('ni_number', models.CharField(serialize=False, validators=[django.core.validators.RegexValidator(message="Must be in the format: 'AA999999A', restrictions to characters apply'", regex='^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\\s*\\d\\s*){6}([A-D]|\\s)$')], max_length=9, primary_key=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('first_name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('dob', models.DateField(default='1990-01-01')),
                ('ni_number', models.CharField(serialize=False, validators=[django.core.validators.RegexValidator(message="Must be in the format: 'AA999999A', restrictions to characters apply'", regex='^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\\s*\\d\\s*){6}([A-D]|\\s)$')], max_length=9, primary_key=True)),
                ('email', models.EmailField(max_length=64)),
                ('middle_name', models.CharField(null=True, max_length=64)),
                ('home_phone', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(message='Not a valid phone number. Up to 9 digits allowed.', regex='^\\+?1?\\d{9,15}$')], max_length=11)),
                ('mob_phone', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(message='Not a valid phone number. Up to 9 digits allowed.', regex='^\\+?1?\\d{9,15}$')], max_length=11)),
                ('cash', models.DecimalField(decimal_places=2, max_digits=20)),
                ('twitter_username', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(message='Not a valid username,please remove @ and max of 15 cahracters', regex='^(\\w){1,15}$')], max_length=15)),
                ('twitter_widget_id', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(message='Not a valid Twitter widget id. must be 18 digits', regex='[\\d]{18}')], max_length=18)),
                ('fa', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('full_name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('buy_date', models.DateField(default='1990-01-01')),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('owner', models.ForeignKey(to='wms.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('symbol', models.CharField(serialize=False, primary_key=True, max_length=5)),
                ('company', models.CharField(max_length=64)),
                ('market', models.ForeignKey(to='wms.Market')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='share',
            name='stock',
            field=models.ForeignKey(to='wms.Stock'),
            preserve_default=True,
        ),
    ]
