# Generated by Django 3.2 on 2021-06-19 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NestedResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.collection')),
            ],
        ),
        migrations.CreateModel(
            name='NestedCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.collection')),
            ],
        ),
    ]
