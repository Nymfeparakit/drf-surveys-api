# Generated by Django 2.2.10 on 2021-07-17 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20210716_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='survey_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.Survey'),
        ),
        migrations.AlterField(
            model_name='questionchoice',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='surveys.Question'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useranswersquestion',
            name='answer_text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='useranswersquestion',
            name='choice_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.QuestionChoice'),
        ),
        migrations.CreateModel(
            name='UserTakesSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.SimpleUser')),
            ],
        ),
    ]