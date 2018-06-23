# Generated by Django 2.0.2 on 2018-06-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180619_0626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='textSnippet',
            new_name='description',
        ),
        migrations.AddField(
            model_name='books',
            name='avgRating',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='pageCount',
            field=models.IntegerField(null=True),
        ),
    ]