# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0004_rides'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crimes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True)),
                ('offense', models.CharField(max_length=180)),
                ('surname', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Rides',
        ),
        migrations.RemoveField(
            model_name='result',
            name='created',
        ),
        migrations.RemoveField(
            model_name='result',
            name='result',
        ),
        migrations.RemoveField(
            model_name='result',
            name='result_name',
        ),
    ]
