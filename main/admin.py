from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('name', 'duration', 'price')
    list_filter = ('name', 'price')
