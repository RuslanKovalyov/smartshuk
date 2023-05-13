from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid

from main.models import Subscription


# def validate_first_name(value):
#     if not value:
#         raise ValidationError('.נא להזין את שם הפרטי שלך') # eng. Please enter your first name.

def validate_bio_length(value):
    word_count = len(value.split())
    if word_count > 1000:
        raise ValidationError('.הביוגרפיה חייבת להיות באורך של 1000 מילים או פחות') # eng. The bio must be 1000 words or less.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-is_staff", "email"]
        verbose_name = 'משתמש' # eng. User
        verbose_name_plural = 'משתמשים' # eng. Users

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #chek for urlsafe uuid
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # payed subscription plan
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='מנוי')
    # auto renew subscription
    auto_renew_subscription = models.BooleanField(default=False, verbose_name='חידוש אוטומטי')
    # verified person by phone number
    verified = models.BooleanField(default=False, verbose_name='מאומת')
    phone_number = models.CharField(max_length=17, null=True, blank=True,verbose_name='מספר טלפון')
    
    avatar = models.ImageField(upload_to='media/user-uploads/avatars', null=True, blank=True)# create save method to resize image and store it on aws s3
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name  = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(blank=True, validators=[validate_bio_length])

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Profile.
        """
        return reverse('profile_detail', args=[str(self.id)])#id? change to unic username for god url link

    def __str__(self):
        return f"{self.user}" # as {self.first_name}'s Profile""


    class Meta:
        ordering = ["first_name"]
        verbose_name = 'פרופיל' # eng. Profile
        verbose_name_plural = 'פרופילים' # eng. Profiles
    
    #on Delete use @receiver
    
#delete the objects associated with the profile model
from django.dispatch import receiver
from django.db.models.signals import post_delete
@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()