from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)

    objects = UserManager()
    active_for_verify = models.BooleanField(default=False)
    code = models.CharField(max_length=5)

    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self) -> str:
        return self.email
    
    def referral_action(self,code):
        try:
            ref = Referral.objects.get(code=code)
            ref.invited.add(self)
            ref.save()
        except Referral.DoesNotExist:
            pass
    
    
class Referral(models.Model):
    user = models.OneToOneField(User,related_name='referral',on_delete=models.CASCADE,blank=True,null=True)
    invited = models.ManyToManyField(User,related_name='ref_address')
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.code   

    
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="profile" 
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"