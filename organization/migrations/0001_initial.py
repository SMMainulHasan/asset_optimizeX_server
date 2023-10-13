# Generated by Django 4.2.6 on 2023-10-13 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='addMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Contributor', 'Contributor'), ('Consumer', 'Consumer')], max_length=100)),
                ('is_company', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(max_length=1000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('organization_logo', models.ImageField(blank=True, null=True, upload_to='images/company-logo/')),
                ('tc', models.BooleanField()),
                ('is_company', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=50)),
                ('company_phone_number', models.IntegerField(unique=True)),
                ('member', models.ManyToManyField(through='organization.addMember', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_organizations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='addmember',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='addmember',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
