# Generated by Django 4.1.2 on 2022-10-11 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='amenities',
        ),
        migrations.AddField(
            model_name='hotel',
            name='amenities',
            field=models.ManyToManyField(to='Home.amenities'),
        ),
    ]
