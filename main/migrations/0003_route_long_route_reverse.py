# Generated by Django 5.2 on 2025-05-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_bus_brand_remove_route_bus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='long_route_reverse',
            field=models.ManyToManyField(related_name='long_route_name_reverse', to='main.longroutename'),
        ),
    ]
