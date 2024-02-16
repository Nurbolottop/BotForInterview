# models.py

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.secondary.models import Nap, Status

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="ФИО студента")
    direction = models.ForeignKey(Nap, on_delete=models.CASCADE, verbose_name="Направление")
    user_id = models.IntegerField(unique=True, verbose_name="ID пользователя telegram")
    chat_id = models.IntegerField(unique=True, verbose_name="Чат ID")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус", blank=True, null=True)
    interview_started = models.BooleanField(default=False, verbose_name="Собеседование начато")
    total_score = models.FloatField(default=0.0, verbose_name="Общий счет баллов")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "1) Студенты"
        verbose_name_plural = "1) Студенты"

@receiver(pre_save, sender=UserProfile)
def update_status(sender, instance, **kwargs):
    if instance.total_score >= 9.0:
        # Находим объект Status с названием "Прошел собеседование"
        passed_status = Status.objects.get(title="Прошел собеседование")
        # Присваиваем его полю status
        instance.status = passed_status
    # else:
        # # Находим объект Status с названием "Не прошел собеседование"
        # not_passed_status = Status.objects.get(title="Не прошел собеседование")
        # # Присваиваем его полю status
        # instance.status = not_passed_status

class TelegramUser(models.Model):
    id_user = models.CharField(
        max_length=100,
        verbose_name="ID пользователя telegram"
    )
    username = models.CharField(
        max_length=255,
        verbose_name="Имя пользователя",
        blank=True, null=True
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия",
        blank=True, null=True
    )
    chat_id = models.CharField(
        max_length=100,
        verbose_name="Чат ID"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = " Пользователь телеграм"
        verbose_name_plural = " Пользователи телеграма"
        