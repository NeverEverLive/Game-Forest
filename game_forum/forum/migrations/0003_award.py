# Generated by Django 3.2.9 on 2021-12-04 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_company_developer_genre_publisher_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
    ]
