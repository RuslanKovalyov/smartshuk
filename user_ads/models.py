from django.db import models
from django.urls import reverse
from location_field.models.plain import PlainLocationField
import datetime
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from smartshuk.settings import AUTH_USER_MODEL, MEDIA_URL, VALID_IMAGE_EXTENSIONS, DATA_UPLOAD_MAX_MEMORY_SIZE
# image processing
from own_libs import image_processing
from PIL import Image, ImageOps
import os
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from user.models import CustomUser
from django.core.files.storage import default_storage
import uuid
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from pillow_heif import register_heif_opener
# delete multiple objects
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

register_heif_opener()


def validate_file_size(value):
    if value.size > DATA_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(f"גודל הקובץ חייב להיות לא יותר מ {DATA_UPLOAD_MAX_MEMORY_SIZE // (1024 * 1024)} MB.")




class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    picture = models.ImageField(    blank=False,
                                    max_length= 500, # 100 
                                    verbose_name='תמונה ראשית',
                                    validators=[
                                            FileExtensionValidator(allowed_extensions=VALID_IMAGE_EXTENSIONS),
                                            validate_file_size,
                                        ],
                                )
    has_album = models.BooleanField(blank=True, default=False) # delete this field
    
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True,)
    title = models.CharField(verbose_name='כותרת', max_length=50, blank=True)
    description = models.TextField(verbose_name='תיאור (טקסט חופשי)', max_length=1000, blank=True)

    # phone_regex = RegexValidator(
    #     regex=r'^\+?1?\d{9,15}$',
    #     # message="Phone number must be entered in the format: '972520000000+ or '0540000000. Up to 15 digits allowed."
    #     message="מספר הטלפון חייב להיכנס בפורמט: '+972520000000 או '0540000000. עד 15 ספרות מותרות."
    # )
    phone_regex = RegexValidator(
        regex=r'^\+?1?[\d\s-]{9,15}$',
        message="מספר הטלפון חייב להיכנס בפורמט: 97252-0000000+ או 0520000000 עד 15 ספרות, רווחים ומקפים מותרים."
    )


    phone = models.CharField(validators=[phone_regex], verbose_name='טלפון', max_length=17, blank=True)
    
    class Meta:
        abstract = True #Cannot create instances of that model directly
    
    # chek for floor < house and ather...
    #!ADD!# limit on format, archive and size when uploading
    def save(self, *args, **kwargs):
        if self.picture:
            if self.pk:
                current_obj = self.__class__.objects.get(pk=self.pk)
                if current_obj.picture != self.picture:
                    current_obj.picture.delete(save=False)

            unique_id = uuid.uuid4().hex
            timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_filename = f"{timestamp}_{unique_id}.jpg"

            self.picture.field.upload_to = f'media/user-uploads/{self.__class__.__name__}'

            img = Image.open(self.picture)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img = ImageOps.exif_transpose(img)
            max_px = 800
            if img.width > max_px or img.height > max_px:
                img.thumbnail((max_px, max_px))

            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)

            self.picture.save(new_filename, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)


    #chack box on Delete not work!!! add signals
    def delete(self, *args, **kwargs):
        #delete avatar
        # print(f"Delete: avatar: {self.picture}")
        try:
            # Delete the object from S3
            key = f'{self.picture}'
            if default_storage.exists(key):
                default_storage.delete(key)
                #print(f"Deleted: {key}")
            else:
                #print(f"File not found: {key}")
                pass
                    
        except Exception as e:
            #print(f"Exception while deleting the picture: {e}")
            pass
        super().delete(*args, **kwargs)

class Region(models.Model):
    """List of Region options"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        ordering = ['name']

    def __str__(self):
        return self.name

class City(models.Model):
    """List of Cities options"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name

class RealEstateCategory(models.Model):
    """List of RealEstate options (New Home, Apartments for rent, Garag, Commercial, Etc). Only for Admin Panel"""
    name = models.CharField(verbose_name='Real estate category', max_length=100)
    singular_name = models.CharField(verbose_name='Real estate singular name of category', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Real estate category'
        verbose_name_plural = 'Real estate categories'
        ordering = ['-name']

    def __str__(self):
        return self.name

class RealEstateDeal(models.Model):  # for realEstate
    """List of Deal types (bay, rent, change ... etc"""
    name = models.CharField(verbose_name='Real estate deal type', max_length=100)

    class Meta:
        verbose_name = 'Real estate deal type'
        verbose_name_plural = 'Real estate deal_types'
        ordering = ['-name']

    def __str__(self):
        return self.name

class RealEstate(Ad):
    #...
    category = models.ForeignKey(RealEstateCategory, verbose_name='קטגוריה', on_delete=models.CASCADE)
    deal_type = models.ForeignKey(RealEstateDeal, verbose_name='סוג העסקה', on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name='עיר', on_delete=models.CASCADE)
    #album = models.OneToOneField(ImageAlbum, on_delete=models.CASCADE)
    address = models.CharField(verbose_name='כתובת',max_length=255)
    cost = models.IntegerField(verbose_name='מחיר', validators=[MinValueValidator(0), MaxValueValidator(100000000)]) # -1 = auction
    rooms = models.SmallIntegerField(verbose_name='מספר חדרים', validators=[MinValueValidator(0), MaxValueValidator(100)])# 0 = studio
    floor = models.SmallIntegerField(verbose_name='קומה', validators=[MinValueValidator(-10), MaxValueValidator(100)])
    size_m2 = models.PositiveSmallIntegerField(verbose_name='שטח (במ״ר)', validators=[MinValueValidator(0), MaxValueValidator(1000)])
    number_floors_in_house = models.PositiveSmallIntegerField(verbose_name='מספר הקומות במבנה', validators=[MinValueValidator(1), MaxValueValidator(100)])
    CheckIn_date_from = models.DateField(verbose_name='תאריך כניסה', default=datetime.date.today, blank=True)

    is_new = models.BooleanField(verbose_name='הנכס חדש', default=False)
    renovated = models.BooleanField(verbose_name='לאחר שיפוץ', default=False)
    furnished = models.BooleanField(verbose_name='מרוהט', default=False)
    balcony = models.BooleanField(verbose_name='עם מרפסת', default=False)
    bunker = models.BooleanField(verbose_name='עם ממ"ד', default=False)
    storage = models.BooleanField(verbose_name='מחסן', default=False)
    conditioner = models.BooleanField(verbose_name='מזגן', default=False)
    elevator = models.BooleanField(verbose_name='מעלית', default=False)
    parking = models.BooleanField(verbose_name='חניה', default=False)
    water_heater = models.BooleanField(verbose_name='דוד שמש', default=False)
    disabled_access = models.BooleanField(verbose_name='גישה לנכים', default=False)
    # without_intermediaries = models.BooleanField(verbose_name='without intermediaries', default=False,)
    # verified seller
    exclusive = models.BooleanField(verbose_name='בלעדי', default=False)

    @property
    def is_past_due(self):
        return date.today() > self.CheckIn_date_from
    
    def delete(self, *args, **kwargs):
        # Delete all related pictures of ulbum
        for picture in self.pictures.all():
            picture.delete()

        # Call the delete method of the parent class Ad
        super(RealEstate, self).delete(*args, **kwargs)

    class Meta:
        verbose_name ='Real estate' #'נדל"ן'
        verbose_name_plural = 'Real estate' #'נדל"ן'
        ordering = ['category', 'deal_type', 'city']

    def __str__(self):
        return self.category.name + ', ' + self.deal_type.name + ' : ' + self.city.name
    
class RealEstatePicture(models.Model):
    ad = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to = 'media/user-uploads/albums')

    class Meta:
        verbose_name = 'תמונה'
        verbose_name_plural = 'תמונות נוספות (עד 10 תמונות)'

    def __str__(self):
        return self.picture.name
    
    def save(self, *args, **kwargs):
        if self.picture:
            if self.pk:
                current_obj = self.__class__.objects.get(pk=self.pk)
                if current_obj.picture != self.picture:
                    current_obj.picture.delete(save=False)

            unique_id = uuid.uuid4().hex
            timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_filename = f"{timestamp}_{unique_id}.jpg"

            img = Image.open(self.picture)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img = ImageOps.exif_transpose(img)
            max_px = 800
            if img.width > max_px or img.height > max_px:
                img.thumbnail((max_px, max_px))

            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            buffer.seek(0)

            self.picture.save(new_filename, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # print("delete picture()")
        try:
            # Delete the object from S3
            key = f'{self.picture}'
            if default_storage.exists(key):
                default_storage.delete(key)
                # print("deleted from S3")
            else:
                # print("not found in S3")
                pass
                    
        except Exception as e:
            # print(f"Exception while deleting the picture: {e}")
            pass
        super().delete(*args, **kwargs)

class RealEstateLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likesRealEstate')
    ad = models.ForeignKey(RealEstate, on_delete=models.CASCADE, related_name='likesRealEstate')

    class Meta:
        verbose_name = 'נדל"ן לייק'
        verbose_name_plural = 'נדל"ן לייקים'

    def __str__(self):
        return str(self.ad.category.name + ' ' + self.ad.deal_type.name + ' ' + self.ad.city.name)

@receiver(post_delete, sender=RealEstate)
def delete_real_estate_media(sender, instance, **kwargs):
    # Delete associated picture of the parent class Ad
    try:
        default_storage.delete(str(instance.picture))
    except:
        # write to errors log file
        pass

    # Delete all related pictures of the RealEstate object
    for picture in instance.pictures.all():
        try:
            default_storage.delete(str(picture.picture))
        except:
            # write to errors log file
            pass
        
@receiver(post_delete, sender=RealEstatePicture)
def delete_real_estate_picture_media(sender, instance, **kwargs):
    try:
        # Delete the object from S3
        default_storage.delete(str(instance.picture))
    except Exception as e:
        # write to errors log file
        pass


#logfile of non existent cities
class NonExistentCity(models.Model):
    city_name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city_name} ({self.count})"