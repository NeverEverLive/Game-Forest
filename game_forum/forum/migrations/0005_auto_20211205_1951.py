# Generated by Django 3.2.9 on 2021-12-05 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20211205_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screenshot',
            name='game',
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='forum.screenshot'),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='file',
            field=models.ImageField(max_length=200, upload_to=''),
        ),
    ]
