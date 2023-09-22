from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from netmagics.models import ActivityTracker
from .models import NetmagicsAdmin
# from globals import current_global_user



#signal for netmagics admin
@receiver(pre_save, sender=NetmagicsAdmin)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = NetmagicsAdmin.objects.get(pk=instance.pk)
    except NetmagicsAdmin.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in NetmagicsAdmin._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields


@receiver(post_save, sender=NetmagicsAdmin)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"NetmagicsAdmin created with name: {instance.user.name} and email: {instance.user.email}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"NetmagicsAdmin updated - {changes_description}")