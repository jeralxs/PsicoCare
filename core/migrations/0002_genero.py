# Generated by Django 5.0.6 on 2024-06-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('idgenero', models.IntegerField(primary_key=True, serialize=False)),
                ('n_genero', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'generopsicologo',
                'managed': False,
            },
        ),
    ]
