# Generated by Django 2.2.6 on 2019-12-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0007_auto_20191212_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='lore',
            field=models.TextField(default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]