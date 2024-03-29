# Generated by Django 2.0.5 on 2018-11-04 22:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import pgqueue.models


class Migration(migrations.Migration):

    dependencies = [
        ('pgqueue', '0002_job_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='context',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=pgqueue.models.lazy_empty_dict),
        ),
        migrations.AlterField(
            model_name='job',
            name='kwargs',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=pgqueue.models.lazy_empty_dict),
        ),
    ]
