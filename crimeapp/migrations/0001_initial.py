# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Select a task to record', max_length=100, verbose_name=b'Task name')),
                ('history', jsonfield.fields.JSONField(default={}, help_text='JSON containing the tasks history', verbose_name='history')),
            ],
            options={
                'verbose_name': 'Task History',
                'verbose_name_plural': 'Task Histories',
            },
            bases=(models.Model,),
        ),
    ]
