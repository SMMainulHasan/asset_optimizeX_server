# Generated by Django 4.2.5 on 2023-10-02 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_company',
        ),
    ]
