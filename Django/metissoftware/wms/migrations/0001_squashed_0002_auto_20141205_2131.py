# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('wms', '0001_initial'), ('wms', '0002_auto_20141205_2131')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FA',
            fields=[
                ('first_name', models.CharField(max_length=64, default='**DEFAULT**')),
                ('surname', models.CharField(max_length=64, default='**DEFAULT**')),
                ('dob', models.DateField(default='1990-01-01')),
                ('ni_number', models.CharField(max_length=9, serialize=False, default='DEFAULT', primary_key=True)),
                ('email', models.EmailField(max_length=64, default='**DEFAULT**')),
                ('mob_number', models.CharField(max_length=11, null=True)),
                ('off_number', models.CharField(max_length=11, null=True)),
                ('password', models.CharField(max_length=64, default='**DEFAULT**')),
            ],
            options={
                'abstract': False,
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
            name='Share',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
        migrations.RemoveField(
            model_name='client',
            name='id',
        ),
        migrations.AddField(
            model_name='client',
            name='cash',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='dob',
            field=models.DateField(default='1990-01-01'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='fa',
            field=models.ForeignKey(default=0, to='wms.FA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='home_phone',
            field=models.CharField(max_length=11, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='middle_name',
            field=models.CharField(max_length=64, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='mob_phone',
            field=models.CharField(max_length=11, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='ni_number',
            field=models.CharField(max_length=9, serialize=False, default='DEFAULT', primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=64, default='**DEFAULT**'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(max_length=64, default='**DEFAULT**'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='surname',
            field=models.CharField(max_length=64, default='**DEFAULT**'),
            preserve_default=True,
        ),
    ]
