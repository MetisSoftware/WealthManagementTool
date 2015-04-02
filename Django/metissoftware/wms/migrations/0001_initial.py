# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import django.utils.timezone


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
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(unique=True, max_length=64)),
                ('first_name', models.CharField(default='**DEFAULT**', max_length=64)),
                ('middle_name', models.CharField(blank=True, max_length=64)),
                ('surname', models.CharField(default='**DEFAULT**', max_length=64)),
                ('image', models.ImageField(default='/media/person-placeholder.png', upload_to='fa_images')),
                ('dob', models.DateField(default='1990-01-01')),
                ('ni_number', models.CharField(validators=[django.core.validators.RegexValidator(regex='^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\\s*\\d\\s*){6}([A-D]|\\s)$', message="Must be in the format: 'AA999999A', restrictions to characters apply'")], max_length=9, serialize=False, primary_key=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', blank=True, verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', help_text='Specific permissions for this user.', related_name='user_set', blank=True, verbose_name='user permissions')),
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
                ('middle_name', models.CharField(blank=True, max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('image', models.ImageField(default='/media/person-placeholder.png', upload_to='client_images')),
                ('dob', models.DateField(default='1990-01-01')),
                ('ni_number', models.CharField(validators=[django.core.validators.RegexValidator(regex='^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\\s*\\d\\s*){6}([A-D]|\\s)$', message="Must be in the format: 'AA999999A', restrictions to characters apply'")], max_length=9, serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=64)),
                ('home_phone', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='Not a valid phone number. Up to 9 digits allowed.')], max_length=11)),
                ('mob_phone', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='Not a valid phone number. Up to 9 digits allowed.')], max_length=11)),
                ('cash', models.DecimalField(max_digits=20, decimal_places=2)),
                ('twitter_username', models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='^(\\w){1,15}$', message='Not a valid username,please remove @ and max of 15 cahracters')], max_length=15)),
                ('facebook_username', models.CharField(blank=True, null=True, max_length=15)),
                ('linkedin_username', models.CharField(blank=True, null=True, max_length=15)),
                ('googleplus_username', models.CharField(blank=True, null=True, max_length=15)),
                ('fa', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('startDateTime', models.DateTimeField()),
                ('endDateTime', models.DateTimeField()),
                ('type', models.CharField(default='meeting', max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('client', models.ForeignKey(to='wms.Client', blank=True, null=True)),
                ('fa', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('name', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingNotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('note', models.TextField()),
                ('event', models.OneToOneField(null=True, to='wms.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date', models.DateField(default='1990-01-01')),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('buy', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(to='wms.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('symbol', models.CharField(max_length=5, serialize=False, primary_key=True)),
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
