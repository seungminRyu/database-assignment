# Generated by Django 4.0 on 2021-12-22 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_students'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.DeleteModel(
            name='Students',
        ),
    ]