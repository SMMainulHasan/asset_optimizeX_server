# Generated by Django 4.2.6 on 2023-10-30 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0011_alter_feedbackmodel_organization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmodel',
            name='feedback_approve',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
