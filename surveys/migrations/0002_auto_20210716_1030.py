# Generated by Django 2.2.10 on 2021-07-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateField(),
        ),
    ]
