# Generated by Django 3.2.9 on 2021-12-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20211210_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
