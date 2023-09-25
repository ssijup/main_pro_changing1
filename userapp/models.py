from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from association.models import Court
from association.models import AssociationSuperAdmin
# from lawfirm.models import LawfirmAdmin
from netmagics.models import NetmagicsAdmin

class UserManager(BaseUserManager):
    use_in_migration = True
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(email, password, **extra_fields)

class UserData(AbstractUser):
    username = None
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.IntegerField(default='725892')
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return self.name
    def has_related_objects(self):
        # has_registrar = Registrar.objects.filter(user=self).exists()
        # has_advocate = Advocate.objects.filter(user=self).exists()
        # has_association_super_admin = AssociationSuperAdmin.objects.filter(user=self).exists()
        # has_netmagics_admin = NetmagicsAdmin.objects.filter(user=self).exists()
        # # has_association_admin = LawfirmAdmin.objects.filter(user=self).exists()
        # if(has_registrar):
        #     return {'data':'registrar'}
        # elif(has_advocate):
        #     return {'data':'advocate'}
        # elif(has_association_super_admin):
        #     return {'data':'association_super_admin'}
        # elif(has_netmagics_admin):
        #     return {'data':'netmagics_admin'}
        # else:
        #     return {'data': None}
        related_objects = {
            'registrar': False,
            'advocate': False,
            'association_super_admin': False,
            'netmagics_admin': False,
        }

        if Registrar.objects.filter(user=self).exists():
            related_objects['registrar'] = True

        if Advocate.objects.filter(user=self).exists():
            related_objects['advocate'] = True

        if AssociationSuperAdmin.objects.filter(user=self).exists():
            related_objects['association_super_admin'] = True

        if NetmagicsAdmin.objects.filter(user=self).exists():
            related_objects['netmagics_admin'] = True

        return related_objects
    
    def __str__(self):
        return self.email+" , "+self.name +","+str(self.id)


USER_CHOICES = (
    ('normal_advocate', 'Normal Advocate'),
    ('normal_admin', 'Normal Admin'),
    ('super_admin', 'Super Admin'),
)    

class Advocate(models.Model):
    user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone=models.CharField(max_length=200)
    enrollment_id=models.CharField(max_length=200)
    specialization=models.CharField(max_length=200)
    address=models.CharField(max_length=200,default='not given')
    profile_image=models.ImageField(upload_to='media/', null=True, blank=True)
    document_image=models.ImageField(upload_to='media/', null=True, blank=True)
    is_suspend=models.BooleanField(default=False)
    type_of_user = models.CharField(max_length=255,choices=USER_CHOICES,default='normal_advocate')
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email+" , "+self.type_of_user +","+str(self.id)
    

class Registrar(models.Model):
    user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    court=models.ForeignKey(Court,on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200,default='not given')
    profile_image=models.ImageField(upload_to='media/', null=True, blank=True)
    def __str__(self): 
        return self.user.email + "," + str(self.id)