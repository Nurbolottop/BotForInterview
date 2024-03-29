# Generated by Django 5.0.2 on 2024-02-06 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary', '0002_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secondary.nap', verbose_name='Направление')),
            ],
            options={
                'verbose_name': '1) Добавить Вопрос',
                'verbose_name_plural': '1)Добавить Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='название статуса')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quations', to='secondary.question')),
            ],
            options={
                'verbose_name': 'Вопросы',
                'verbose_name_plural': 'Вопросы',
            },
        ),
    ]
