# Generated by Django 4.2.6 on 2023-10-25 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_organization_invited_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='invited_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
