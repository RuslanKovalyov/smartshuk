from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

admin.site.site_header = "Administration"
#admin.site.index_title = "dministration"
#admin.site.site_title = "administration"

#admin.site.register(CustomUsers)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', ('date_joined', 'last_login'))}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    search_fields = ('email',)
    ordering = ('-is_staff', 'email')

#admin.site.register(Profiles)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'first_name', 'phone_number', 'subscription', 'auto_renew_subscription', 'verified')
    list_filter = ('subscription', 'user')
    readonly_fields = ('user',)
    # fields = [('user', 'first_name'), ( ), ]
