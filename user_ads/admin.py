from django.contrib import admin
from .models import Region, City, RealEstateCategory, RealEstateDeal, RealEstate, RealEstatePicture, RealEstateLike

#logfiles
from .models import NonExistentCity

# Register models.
admin.site.register(Region)
admin.site.register(City)
admin.site.register(RealEstateCategory)
admin.site.register(RealEstateDeal)
admin.site.register(RealEstate)
admin.site.register(RealEstateLike)

#logfile in db
class NonExistentCityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'count')
    ordering = ('-count',)

admin.site.register(NonExistentCity, NonExistentCityAdmin)

# Register models with custom admin.
@admin.register(RealEstatePicture)
class RealEstatePictureAdmin(admin.ModelAdmin):
    model = RealEstatePicture
    list_display = ('ad', 'picture')
    list_filter = ('ad', 'picture')
    fields = [('ad', 'picture'), ( ), ]

    search_fields = ('ad', 'picture')
    ordering = ('-ad', 'picture')
