# Generated by Django 2.2.10 on 2021-07-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0012_auto_20210718_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateField(),
        ),
    ]
