# Generated by Django 2.0.2 on 2018-06-26 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
