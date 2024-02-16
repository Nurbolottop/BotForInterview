from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from .models import Status, Nap

@receiver(pre_migrate)
def create_default_objects(sender, app_config, **kwargs):
    if app_config.name == 'apps.secondary':
        if not Status.objects.exists():
            Status.objects.create(title="Активный")
            Status.objects.create(title="Неактивный")
            Status.objects.create(title="Выпускник")
            Status.objects.create(title="Прошел собеседование")
            Status.objects.create(title="Не прошел собеседование")
            print("Созданы стандартные статусы.")

        if not Nap.objects.exists():
            Nap.objects.create(title="Backend")
            Nap.objects.create(title="Frontend")
            Nap.objects.create(title="UXUI")
            Nap.objects.create(title="Android")
            # Добавьте другие направления, если необходимо
            print("Созданы стандартные направления.")
