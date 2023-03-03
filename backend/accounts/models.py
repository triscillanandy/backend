
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None,is_active=True,is_staff=False,is_admin=False):
        
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('users must have password')
            
        user_obj = self.model(
            email=self.normalize_email(email),
           
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active= is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        
        return user

    def create_superuser(self, email, password=None):
        
        user = self.create_user(
           
            email,
            password=password,
            is_staff = True,
            is_admin = True
        )
       
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True, null=True)
    username = models.CharField(max_length=150,unique=150, null=True)
    
    first_name=models.CharField(max_length=200,blank=True,null=True)
    last_name=models.CharField(max_length=200,blank=True,null=True)
    #delvery details
    phone=models.CharField(max_length=150,blank=True)
 
    created_at =  models.DateTimeField(auto_now_add=True) 
    updated= models.DateTimeField(auto_now=True)
    is_email_verified =models.BooleanField(default=False)
    active = models.BooleanField(default=True)#can login
    staff = models.BooleanField(default=False) # a staff user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    

    USERNAME_FIELD = 'email'#username
    REQUIRED_FIELDS = []

    objects =UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        if self.first_name:
            return self.first_name
        if self.first_name:
            return self.first_name    
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

  
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    

    @property
    def is_active(self):
        "Is the user an active admin member?"
        return self.active    
    





 