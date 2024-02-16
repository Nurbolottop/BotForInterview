# Generated by Django 5.0.2 on 2024-02-06 22:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('secondary', '0003_question_questionadd'),
        ('telegram_bot', '0008_userprofile_interview_started'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Ответ пользователя')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secondary.questionadd', verbose_name='Вопрос')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.userprofile', verbose_name='Профиль пользователя')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос',
                'verbose_name_plural': 'Ответы на вопросы',
            },
        ),
    ]