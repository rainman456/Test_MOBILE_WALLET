# Generated by Django 3.2.7 on 2023-07-18 11:03

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='NG', max_length=2),
        ),
    ]
