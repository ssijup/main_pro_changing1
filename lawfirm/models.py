from django.db import models
from userapp.models import UserData


LAWFIRM_INVITATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
    ]

class LawFirm(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    contact_no=models.CharField(max_length=200)
    specialization=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    estd_date=models.DateField(default='2000-01-01')
    created_by =models.ForeignKey('userapp.Advocate',on_delete=models.CASCADE, related_name='created_lawfirms')
    is_suspend=models.BooleanField(default= False)
    email = models.EmailField(default = 'default@gmail.com')
    def __str__(self):
        return self.name+","+str(self.id)


class LawfirmAdmin(models.Model):
    user = models.ForeignKey('userapp.UserData',on_delete=models.CASCADE)
    lawfirm = models.ForeignKey(LawFirm,on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200,default='not given')
    profile_image=models.ImageField(upload_to='media/', null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email
    

class AdvocateLawfirm(models.Model):
    advocate = models.ForeignKey('userapp.Advocate',on_delete=models.CASCADE)
    advocate_status = models.BooleanField(default=True)
    lawfirm = models.ForeignKey(LawFirm,on_delete=models.CASCADE)
    invitation_status= models.BooleanField(default=False)


class LawfirmNotification(models.Model):
    lawfirm=models.ForeignKey(LawFirm,on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    content=models.TextField()
    created_at=models.DateField(auto_now=True)
