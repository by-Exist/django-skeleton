# Generated by Django 3.2 on 2021-07-01 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("example", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="title",
            field=models.CharField(max_length=20, verbose_name="제목"),
        ),
    ]
