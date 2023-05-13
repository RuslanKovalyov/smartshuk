from django.db import models

# Create your models here.

from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=100, verbose_name='שם התוכנית')  # eng. Plan name
    description = models.TextField(verbose_name='תיאור התוכנית')  # eng. Plan description
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='מחיר')  # eng. Price
    duration = models.DurationField(verbose_name='משך המנוי')  # eng. Subscription duration
    icon = models.ImageField(upload_to='media/subscriptions/icons', null=True, blank=True, verbose_name='אייקון')  # Icon for the plan
    is_default = models.BooleanField(default=False, verbose_name='ברירת מחדל')  # eng. Default plan (free plan)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['price']
        verbose_name = 'מנוי'  # eng. Subscription
        verbose_name_plural = 'מנויים'  # eng. Subscriptions
