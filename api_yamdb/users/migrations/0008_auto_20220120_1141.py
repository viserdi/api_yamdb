# Generated by Django 2.2.16 on 2022-01-20 08:41

import users.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20220120_1126'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.NewUser()),
            ],
        ),
    ]
