from django.db import models
# from userapp.models import UserData


APPROVAL_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

class Court(models.Model):
    name=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    estd_date = models.DateField(default='2000-01-01')
    address=models.CharField(max_length=200)
    contact_no=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    def __str__(self): 
        return self.name+","+str(self.id)


class Jurisdiction(models.Model):
    name=models.CharField(max_length=200)
    area=models.CharField(max_length=200)
    court=models.ForeignKey(Court, on_delete=models.CASCADE)
    def __str__(self): 
        return self.name 
    
class Association(models.Model):
    name=models.CharField(max_length=200)
    estd_date=models.DateField(default='2000-01-01')
    court=models.ForeignKey(Court, on_delete=models.CASCADE)
    address=models.CharField(max_length=200)
    website=models.CharField(max_length=200)
    contact_no=models.CharField(max_length=200)
    email=models.EmailField()
    is_suspend=models.BooleanField(max_length=200,default=False)
    instamojo_API_KEY = models.CharField(max_length=200,default='')
    instamojo_AUTH_TOKEN = models.CharField(max_length=200,default='')
    def __str__(self): 
        return self.name+","+str(self.id)


class MembershipPlan(models.Model):
    duration = models.IntegerField()
    unit_of_plan = models.CharField(max_length=20)
    membership_price = models.CharField(max_length=10 ,default='1')
    association=models.ForeignKey(Association,on_delete=models.CASCADE,default='1')
    def __str__(self): 
        return self.membership_price + "," +str(self.id)



class MembershipFineAmount(models.Model):
    fine_amount = models.IntegerField(default= 500)
    association=models.ForeignKey(Association,on_delete=models.CASCADE,default='1')
    def __str__(self): 
        return str(self.id)


class Notification(models.Model):
    association=models.ForeignKey(Association,on_delete=models.CASCADE, default=0)
    title=models.CharField(max_length=250)
    content=models.TextField()
    created_at=models.DateField(auto_now=True)


class AssociationMembershipPayment(models.Model):
    for_payment_plan =models.ForeignKey(MembershipPlan ,on_delete=models.SET_NULL ,null=True)
    for_user_details = models.ForeignKey('userapp.Advocate' ,on_delete= models.SET_NULL ,null = True,related_name='useradvocate')
    payment_id =models.CharField(max_length=200)
    payment_status = models.BooleanField(default = False)
    payment_done_at = models.DateField(auto_now_add= True)
    payment_expiry_date = models.DateField(default='2000-01-01')
    payment_total_amount_paid = models.IntegerField(default=0)
    payment_status_of_gateway = models.CharField(max_length=25 ,default= 'failed')
    payment_association=models.ForeignKey(Association,on_delete=models.CASCADE, default=0)
    is_current = models.BooleanField(default=False)
    have_fine = models.PositiveIntegerField(default=0)
    def __str__(self):
        return str(self.id)


class AssociationPaymentRequest(models.Model):
    payment_request_id = models.CharField(max_length=300)
    payment_requested_user = models.ForeignKey('userapp.Advocate',on_delete=models.CASCADE)
    payment_requested_plan = models.ForeignKey(MembershipPlan,on_delete=models.CASCADE)
    payment_expiry_date = models.DateField(default='2000-01-01')
    payment_total_amount_paid = models.IntegerField(default=0)
    payment_association=models.ForeignKey(Association,on_delete=models.CASCADE, default=0)
    have_fine = models.PositiveIntegerField(default=0)


class AdvocateAssociation(models.Model):
    advocate = models.ForeignKey('userapp.Advocate',on_delete=models.CASCADE)
    association = models.ForeignKey(Association,on_delete=models.SET_NULL,null=True,blank=True)
    advocate_status = models.BooleanField(default=False)
    approval_status = models.CharField(max_length= 50, choices=APPROVAL_STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey('userapp.UserData', on_delete=models.SET_NULL, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, null = True, blank=True, default ='Not given')



class AssociationSuperAdmin(models.Model):
    user = models.ForeignKey('userapp.UserData',on_delete=models.CASCADE)
    association = models.ForeignKey(Association,on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200,default='not given')
    profile_image=models.ImageField(upload_to='media/', null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    def __str__(self): 
        return self.user.email + "," +str(self.id)


class RawData(models.Model):
    enrollment_id = models.CharField(max_length=25)
    name = models.CharField(max_length=250)
    place_of_pratice= models.CharField(max_length=250)
    





