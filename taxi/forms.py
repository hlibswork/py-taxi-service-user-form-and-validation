from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number", "first_name", "last_name")

    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")

        if len(license_number) != 8:
            raise ValidationError("License must be only of 8 characters.")

        if not license_number[:3].isupper()\
                or not license_number[:3].isalpha():
            raise ValidationError(
                "License first 3 characters must be" " uppercase letters."
            )

        if not license_number[3:].isdigit():
            raise ValidationError("License last 5 characters must be digits")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
