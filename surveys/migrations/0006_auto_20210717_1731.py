# Generated by Django 2.2.10 on 2021-07-17 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20210717_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='survey_id',
            new_name='survey',
        ),
        migrations.RenameField(
            model_name='questionchoice',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='useranswersquestion',
            old_name='choice_id',
            new_name='choice',
        ),
        migrations.RenameField(
            model_name='useranswersquestion',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='usertakessurvey',
            old_name='survey_id',
            new_name='survey',
        ),
        migrations.RenameField(
            model_name='usertakessurvey',
            old_name='user_id',
            new_name='user',
        ),
    ]