from django import forms


class VacancyForm(forms.Form):

    name = forms.CharField(max_length=300)
    phone = forms.CharField()
    position = forms.CharField(max_length=300)
    sumfile = forms.FileField()
