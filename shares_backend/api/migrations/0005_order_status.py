# Generated by Django 3.2 on 2021-05-09 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210507_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
