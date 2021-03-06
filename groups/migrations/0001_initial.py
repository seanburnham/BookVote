# Generated by Django 2.0.2 on 2018-06-26 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_auto_20180620_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('passphrase', models.TextField(null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('admin_users', models.ManyToManyField(related_name='admin_users', to=settings.AUTH_USER_MODEL)),
                ('bookList', models.ManyToManyField(related_name='bookList', to='books.Books')),
                ('currentBook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currentBook', to='books.Books')),
                ('users', models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
