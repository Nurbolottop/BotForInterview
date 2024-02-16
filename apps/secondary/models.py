from django.db import models

# Create your models here.
class Nap(models.Model):
    title = models.CharField(
        max_length = 255,
        verbose_name = "Название направления"
    )
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Добавить напаравление"
        verbose_name_plural = "Добавить напаравление"

class Status(models.Model):
    title = models.CharField(
        max_length = 255,
        verbose_name ="название статуса"
    )
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Добавить Статусы"
        verbose_name_plural = "Добавить Статус"
    
class Question(models.Model):
    direction = models.ForeignKey(Nap, on_delete=models.CASCADE, verbose_name="Направление")


    class Meta:
        verbose_name = "1) Добавить Вопрос"
        verbose_name_plural = "1)Добавить Вопросы"
        
class QuestionAdd(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="quations")
    text = models.CharField(
        max_length = 255,
        verbose_name ="название статуса"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"