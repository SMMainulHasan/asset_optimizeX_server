# Generated by Django 4.2.6 on 2023-10-12 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadAsset', '0006_remove_uploadasset_asset_remove_uploadasset_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadasset',
            name='asset',
            field=models.FileField(null=True, upload_to='images/company/asset/'),
        ),
        migrations.DeleteModel(
            name='AssetFile',
        ),
    ]
