# Generated by Django 3.2.9 on 2021-12-10 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_genre_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='file',
            field=models.ImageField(upload_to='%Y/%m/%d/'),
        ),
    ]
