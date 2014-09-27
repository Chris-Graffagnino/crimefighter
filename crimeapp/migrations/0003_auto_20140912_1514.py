# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0002_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='result_name',
            field=models.CharField(default=b'Jerry', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.CharField(default=b'000', max_length=20),
        ),
    ]
