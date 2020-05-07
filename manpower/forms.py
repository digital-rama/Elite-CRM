from django import forms
from manpower.models import *
from project.models import *
from bootstrap_datepicker_plus import DatePickerInput


class addTender(forms.ModelForm):

    class Meta:
        model = Tender
        fields = '__all__'
        widgets = {
            'tender_submission_date': DatePickerInput(format='%Y-%m-%d'),
            'physical_submission_date': DatePickerInput(format='%Y-%m-%d'),
            'tech_bid_opening_date': DatePickerInput(format='%Y-%m-%d'),
            'bid_price_opening_date': DatePickerInput(format='%Y-%m-%d'),
        }


class otherContractorsForm(forms.ModelForm):
    class Meta:
        model = otherContractors
        fields = '__all__'
        exclude = ['tender']


class addProject(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'
        exclude = ['tender']
        widgets = {
            'project_start_date': DatePickerInput(format='%Y-%m-%d'),
        }

# Supervisor & Labour Forms
# Supervisor & Labour Forms
# Supervisor & Labour Forms


class SupervisorForm(forms.ModelForm):
    class Meta:
        model = SuperVisors
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
            're_password': forms.PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
            'dateofbirth': DatePickerInput(format='%Y-%m-%d')
        }
