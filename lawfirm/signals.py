from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from netmagics.models import ActivityTracker
from .models import ( LawFirm, LawfirmAdmin)


#signal for lawfirm
@receiver(pre_save, sender=LawFirm)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = LawFirm.objects.get(pk=instance.pk)
    except LawFirm.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in LawFirm._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=LawFirm)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"LawFirm created with name: {instance.name} by: {instance.created_by.user.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"LawFirm updated - {changes_description}")


#signal for lawfirm admin
@receiver(pre_save, sender=LawfirmAdmin)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = LawfirmAdmin.objects.get(pk=instance.pk)
    except LawfirmAdmin.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in LawfirmAdmin._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=LawfirmAdmin)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"LawfirmAdmin created with name: {instance.user.name} for lawfirm: {instance.lawfirm.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"LawfirmAdmin updated - {changes_description}")