from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from netmagics.models import ActivityTracker
from .models import ( Court, Jurisdiction, Association, MembershipPlan, MembershipFineAmount, Notification,
                     AssociationMembershipPayment, AssociationPaymentRequest, AdvocateAssociation,
                     AssociationSuperAdmin)

from netmagics.activitymiddleware import get_current_user

#signal for court
@receiver(pre_save, sender=Court)
def model_pre_save(sender, instance, **kwargs):
    # Get the database version of the instance
    try:
        db_instance = Court.objects.get(pk=instance.pk)
    except Court.DoesNotExist:
        # If the instance is new, there are no changes to track
        pass
    else:
        # Compare the fields of the current instance with the database version
        changed_fields = []
        for field in Court._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        
        # Store the changed fields in the instance
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Court)
def model_post_save(sender, instance, created, **kwargs):
    current_user = get_current_user()
    if current_user:
        user_name = str(current_user)
    else:
        user_name = 'unknown'
    if created:
        ActivityTracker.objects.create(description=f"Court created with name: {instance.name} and type: {instance.type}", done_by=user_name)
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Court details updated - {changes_description}", done_by=user_name)

#signal for jurisdiction
@receiver(pre_save, sender=Jurisdiction)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = Jurisdiction.objects.get(pk=instance.pk)
    except Jurisdiction.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in Jurisdiction._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Jurisdiction)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Jurisdiction created with name: {instance.name} and court: {instance.court.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Jurisdiction updated - {changes_description}")

#signal for association
@receiver(pre_save, sender=Association)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = Association.objects.get(pk=instance.pk)
    except Association.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in Association._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Association)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Association created with name: {instance.name} and court: {instance.court.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Association updated - {changes_description}")


#signal for membership plan
@receiver(pre_save, sender=MembershipPlan)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = MembershipPlan.objects.get(pk=instance.pk)
    except MembershipPlan.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in MembershipPlan._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=MembershipPlan)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"MembershipPlan created with price: {instance.membership_price} and association: {instance.association.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"MembershipPlan updated - {changes_description}")


#signal for membership fine amount
@receiver(pre_save, sender=MembershipFineAmount)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = MembershipFineAmount.objects.get(pk=instance.pk)
    except MembershipFineAmount.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in MembershipFineAmount._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=MembershipFineAmount)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"MembershipFineAmount created with name: {instance.fine_amount} and association: {instance.association.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"MembershipFineAmount updated - {changes_description}")


#signal for notification
@receiver(pre_save, sender=Notification)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = Notification.objects.get(pk=instance.pk)
    except Notification.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in Notification._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=Notification)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Notification created with title: {instance.title} and association: {instance.association.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Notification updated - {changes_description}")


#signal for association membership payment
@receiver(pre_save, sender=AssociationMembershipPayment)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = AssociationMembershipPayment.objects.get(pk=instance.pk)
    except AssociationMembershipPayment.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in AssociationMembershipPayment._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=AssociationMembershipPayment)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"AssociationMembershipPayment created with payment id: {instance.payment_id} and status: {instance.payment_status}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"AssociationMembershipPayment updated - {changes_description}")

#signal for association payment request
@receiver(pre_save, sender=AssociationPaymentRequest)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = AssociationPaymentRequest.objects.get(pk=instance.pk)
    except AssociationPaymentRequest.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in AssociationPaymentRequest._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=AssociationPaymentRequest)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"AssociationPaymentRequest created by user: {instance.payment_requested_user} and payment request id: {instance.payment_request_id}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"AssociationPaymentRequest updated - {changes_description}")


#signal for advocate association
@receiver(pre_save, sender=AdvocateAssociation)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = AdvocateAssociation.objects.get(pk=instance.pk)
    except AdvocateAssociation.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in AdvocateAssociation._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=AdvocateAssociation)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Advocate related to Association created with advocate name: {instance.advocate.user.name} and association: {instance.association.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Advocate related to Association updated - {changes_description}")

#signal for association super admin
@receiver(pre_save, sender=AssociationSuperAdmin)
def model_pre_save(sender, instance, **kwargs):
    try:
        db_instance = AssociationSuperAdmin.objects.get(pk=instance.pk)
    except AssociationSuperAdmin.DoesNotExist:
        pass
    else:
        changed_fields = []
        for field in AssociationSuperAdmin._meta.fields:
            if getattr(instance, field.name) != getattr(db_instance, field.name):
                changed_fields.append(field.name)
        instance._changed_fields = changed_fields

@receiver(post_save, sender=AssociationSuperAdmin)
def model_post_save(sender, instance, created, **kwargs):
    if created:
        ActivityTracker.objects.create(description=f"Association Admin created with name: {instance.user.name} and association: {instance.association.name}")
    else:
        if hasattr(instance, '_changed_fields'):
            changed_fields = instance._changed_fields
            if changed_fields:
                changes_description = ", ".join([f"{field}: {getattr(instance, field)}" for field in changed_fields])
                ActivityTracker.objects.create(description=f"Association Admin updated - {changes_description}")