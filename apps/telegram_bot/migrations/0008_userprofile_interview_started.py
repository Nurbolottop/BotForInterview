# Generated by Django 5.0.2 on 2024-02-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0007_alter_userprofile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='interview_started',
            field=models.BooleanField(default=False, verbose_name='Собеседование начато'),
        ),
    ]
