# Generated by Django 3.2 on 2022-11-26 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0002_auto_20221030_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalprofile',
            name='area',
            field=models.TextField(null=True),
        ),
    ]
