from django.db import models
from apps.telegram_bot.models import UserProfile
from apps.secondary.models import QuestionAdd

class InterviewAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Профиль пользователя")
    question = models.ForeignKey(QuestionAdd, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ пользователя")
    score = models.FloatField(default=0, verbose_name="Баллы")  # Добавляем поле для баллов
    
    def save(self, *args, **kwargs):
        if self.pk:  # Проверяем, сохраняется ли уже существующий объект
            # Получаем старый балл за этот ответ на вопрос
            old_score = InterviewAnswer.objects.get(pk=self.pk).score
            # Обновляем общий счет баллов пользователя
            self.user_profile.total_score -= old_score
            self.user_profile.total_score += self.score
            self.user_profile.save()
        else:
            # Если объект только что создан, просто добавляем баллы к общему счету пользователя
            self.user_profile.total_score += self.score
            self.user_profile.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Ответ пользователя {self.user_profile.full_name} на вопрос: {self.question.text}"

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"
