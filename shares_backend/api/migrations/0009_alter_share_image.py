# Generated by Django 3.2 on 2021-05-15 03:14

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210514_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.upload_path),
        ),
    ]
