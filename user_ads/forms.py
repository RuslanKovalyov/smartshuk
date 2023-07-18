import logging
logging.basicConfig(filename="city_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")
from .models import NonExistentCity

from django import forms
from .models import RealEstateCategory, RealEstateDeal, RealEstate, RealEstatePicture, City
from .models import SecondHandCategory, SecondHandSubCategory, SecondHandType, SecondHand, SecondHandPicture
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.core.validators import FileExtensionValidator
from django.conf import settings


def validate_file_size(value):
    max_file_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    if value.size > max_file_size:
        raise ValidationError(f"גודל הקובץ חייב להיות לא יותר מ {max_file_size // (1024 * 1024)} MB.")

accepted_extensions = ",".join([f'image/{ext}' for ext in settings.VALID_IMAGE_EXTENSIONS])

class RealEstate_PostingForm(forms.ModelForm):
    city = forms.CharField(
        required=True,
        label="יישוב:",
        widget=forms.TextInput(attrs={'list': 'city_list'}),
    )

    def clean_city(self):
        city_name = self.cleaned_data['city']
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            non_existent_city, created = NonExistentCity.objects.get_or_create(city_name=city_name)
            non_existent_city.count += 1
            non_existent_city.save()

            raise forms.ValidationError(
                # "The city you entered does not exist in our database. Please select a valid city. We are working on adding more cities over time."
                "העיר שהזנת אינה קיימת במאגר הנתונים שלנו. אנא בחר עיר תקפה. אנחנו עובדים על הוספת ערים נוספות לאורך הזמן."
            )

        return city


    pictures = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': accepted_extensions}), label="תמונות נוספות, עד 10")
    def clean_pictures(self):
        pictures = self.files.getlist('pictures')
        if len(pictures) > 10:
            # raise ValidationError("You can upload a maximum of 10 pictures.")
            raise ValidationError("ניתן להעלות מקסימום 10 תמונות.")
        
        # file_extension_validator = FileExtensionValidator(settings.VALID_IMAGE_EXTENSIONS)

        for picture in pictures:
            validate_file_size(picture)
            # file_extension_validator(picture)

        return pictures
    
    picture = forms.ImageField(
        label='תמונה ראשית',
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': accepted_extensions})
        )

    class Meta:
        model = RealEstate
        # fields = ("__all__")
        fields = ['category','deal_type','city','picture', 'pictures', 'phone','title','description','address','cost','rooms','floor','size_m2','number_floors_in_house','CheckIn_date_from','is_new','renovated','furnished','balcony','bunker','storage','conditioner','elevator','parking','water_heater','disabled_access','exclusive',]
        widgets = {
            'CheckIn_date_from': forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class RealEstate_SearchForm(forms.Form):
    template_name = "user_ads/form_snippets/search_forms/real_estate_form.html"

    category = forms.ModelChoiceField(
        queryset=RealEstateCategory.objects.all(),
        empty_label="כל נכס",
        required=False,
        label="Category",
    )

    deal_type = forms.ModelChoiceField(
        queryset=RealEstateDeal.objects.all(),
        empty_label="סוג העסקה: הכל",
        required=False,
        label="Deal Type",
    )

    city = forms.CharField(required=False, max_length=55,
                           widget=forms.TextInput(attrs={'placeholder': 'בכל עיר', 'list': 'city_list'},))

    # filters
    with_phote_only_toggle = forms.BooleanField(required=False, initial=True)
    max_cost = forms.IntegerField(
        required=False, min_value=0, max_value=1_000_000_000,
        widget=forms.NumberInput(
            attrs={'placeholder': '--- מקסימלי'})
    )
    min_rooms = forms.IntegerField(
        required=False, min_value=0, max_value=6,
        widget=forms.NumberInput(
            attrs={'type': "range", 'value': "0", 'max': "6", 'min': "0", 'step': "1", 'oninput':
                '''this.value=Math.min(this.value,this.parentNode.childNodes[5].value-1);
                var value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
                var children = this.parentNode.childNodes[1].childNodes;
                children[1].style.width=value+'%';
                children[5].style.left=value+'%';
                children[7].style.left=value+'%';children[11].style.left=value+'%';
                children[11].childNodes[1].innerHTML=this.value;'''})
    )

    max_rooms = forms.IntegerField(
        required=False, min_value=0, max_value=6,
        widget=forms.NumberInput(
            attrs={'type': "range", 'value': "6", 'max': "6", 'min': "0", 'step': "1", 'oninput':
                '''this.value=Math.max(this.value,this.parentNode.childNodes[3].value-(-1));
                var value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
                var children = this.parentNode.childNodes[1].childNodes;
                children[3].style.width=(100-value)+'%';
                children[5].style.right=(100-value)+'%';
                children[9].style.left=value+'%';children[13].style.left=value+'%';
                children[13].childNodes[1].innerHTML=this.value;'''})
    )



    # min_floor = forms.ChoiceField(required=False,
    #                               choices=[('', 'מ--')] +
    #                               [(str(namb), namb)
    #                                for namb in range(1, 13)]
    #                               )

    # max_floor = forms.ChoiceField(required=False,
    #                               choices=[('', 'עד--')] +
    #                               [(str(namb), namb)
    #                                for namb in range(1, 13)]
    #                               )




    is_new = forms.BooleanField(required=False, initial=False)
    renovated = forms.BooleanField(required=False, initial=False)
    furnished = forms.BooleanField(required=False, initial=False)
    balcony = forms.BooleanField(required=False, initial=False)
    bunker = forms.BooleanField(required=False, initial=False)
    storage = forms.BooleanField(required=False, initial=False)
    conditioner = forms.BooleanField(required=False, initial=False)
    elevator = forms.BooleanField(required=False, initial=False)
    parking = forms.BooleanField(required=False, initial=False)
    disabled_access = forms.BooleanField(required=False, initial=False)
    without_intermediaries = forms.BooleanField(required=False, initial=False)
    exclusive = forms.BooleanField(required=False, initial=False)

class SecondHand_PostingForm(forms.ModelForm):
    city = forms.CharField(
        required=True,
        label="יישוב:",
        widget=forms.TextInput(attrs={'list': 'city_list'}),
    )

    def clean_city(self):
        city_name = self.cleaned_data['city']
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            non_existent_city, created = NonExistentCity.objects.get_or_create(city_name=city_name)
            non_existent_city.count += 1
            non_existent_city.save()

            raise forms.ValidationError(
                # "The city you entered does not exist in our database. Please select a valid city. We are working on adding more cities over time."
                "העיר שהזנת אינה קיימת במאגר הנתונים שלנו. אנא בחר עיר תקפה. אנחנו עובדים על הוספת ערים נוספות לאורך הזמן."
            )

        return city


    pictures = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': accepted_extensions}), label="תמונות נוספות, עד 10")
    def clean_pictures(self):
        pictures = self.files.getlist('pictures')
        if len(pictures) > 10:
            # raise ValidationError("You can upload a maximum of 10 pictures.")
            raise ValidationError("ניתן להעלות מקסימום 10 תמונות.")
        
        # file_extension_validator = FileExtensionValidator(settings.VALID_IMAGE_EXTENSIONS)

        for picture in pictures:
            validate_file_size(picture)
            # file_extension_validator(picture)

        return pictures
    
    picture = forms.ImageField(
        label='תמונה ראשית',
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': accepted_extensions})
        )

    class Meta:
        model = SecondHand
        # fields = ("__all__")
        fields = ['category','sub_category', 'type', 'brand', 'city','picture', 'pictures', 'phone','title','description','address','cost', 'exclusive']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class SecondHand_SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].to_field_name = 'name'
        self.fields['sub_category'].to_field_name = 'name'
        self.fields['type'].to_field_name = 'name'
        
    template_name = "user_ads/form_snippets/search_forms/secondhand_form.html"

    category = forms.ModelChoiceField(
        queryset=SecondHandCategory.objects.all(),
        empty_label="קטגוריה",
        required=False,
        label="Category",
        widget=forms.Select(attrs={'onchange': "this.form.submit();"})
    )

    # if category is not None:
    sub_category = forms.ModelChoiceField(
        queryset=SecondHandSubCategory.objects.all(),
        empty_label="תת קטגוריה",
        required=False,
        label="Sub Category",
        widget=forms.Select(attrs={'onchange': "this.form.submit();"})
    )

    type = forms.ModelChoiceField(
        queryset=SecondHandType.objects.all(),
        empty_label="סוג",
        required=False,
        label="Type",
        widget=forms.Select(attrs={'onchange': "this.form.submit();"})
    )

    # filters
    exclusive = forms.BooleanField(required=False, initial=False)
