# Generated by Django 2.0.2 on 2018-06-28 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_group_currentbookdeadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='passphrase',
        ),
    ]