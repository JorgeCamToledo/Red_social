# Generated by Django 4.2.6 on 2023-10-14 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0003_rename_aprroved_follower_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='approved',
        ),
    ]
