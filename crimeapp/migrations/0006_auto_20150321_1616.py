# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeapp', '0005_auto_20140926_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crimes',
            options={'verbose_name_plural': 'crimes'},
        ),
    ]
