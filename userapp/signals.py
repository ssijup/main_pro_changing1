from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from netmagics.models import ActivityTracker
from .models import Advocate, Registrar


#signal for advocate
@receiver(pre_save, sender=Advocate)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = Advocate.objects.get(pk=instance.pk)
    except Advocate.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in Advocate._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Advocate)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Advocate created with name: {instance.user.name} and email: {instance.user.email}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Advocate updated - {changes_description}")


#signal for registrar
@receiver(pre_save, sender=Registrar)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = Registrar.objects.get(pk=instance.pk)
    except Registrar.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in Registrar._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Registrar)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Registrar created with name: {instance.user.name} and email: {instance.user.email}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Registrar updated - {changes_description}")