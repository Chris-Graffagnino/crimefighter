# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0003_auto_20140912_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rides',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d', models.DecimalField(max_digits=5, decimal_places=2)),
                ('s', models.DateTimeField()),
                ('e', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
