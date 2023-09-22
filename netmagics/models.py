from django.db import models

class NetmagicsAdmin(models.Model):
    user = models.ForeignKey('userapp.UserData',on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone=models.CharField(max_length=200,null=True, blank=True)
    address=models.CharField(max_length=200,default='not given')
    profile_image=models.ImageField(upload_to='media/', null=True, blank=True) 
    is_owner = models.BooleanField(default=False)
    def __str__(self): 
        return self.user.email+","+str(self.id)
    
    
class ActivityTracker(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    done_by=models.CharField(max_length=250,default='unknown')
    