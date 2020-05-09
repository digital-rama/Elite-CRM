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


class addProjectStart(forms.ModelForm):
    class Meta:
        model = ProjectStart
        fields = '__all__'
        exclude = ['project']
        widgets = {
            'ai_sub_date': DatePickerInput(format='%Y-%m-%d'),
            'ahts': DatePickerInput(format='%Y-%m-%d'),
            'asd': DatePickerInput(format='%Y-%m-%d'),
        }


class securityDeposit(forms.ModelForm):
    class Meta:
        model = Security_Deposit
        fields = '__all__'
        exclude = ['project']
        widgets = {
            'cretion_date': DatePickerInput(format='%Y-%m-%d'),
            'submission_date': DatePickerInput(format='%Y-%m-%d'),
            'validity': DatePickerInput(format='%Y-%m-%d'),
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


class projectRep(forms.ModelForm):
    class Meta:
        model = ProjectRepeter
        fields = '__all__'
        exclude = ['project']
        widgets = {
            'from_date': DatePickerInput(format='%Y-%m-%d'),
            'to_date': DatePickerInput(format='%Y-%m-%d'),
            'doc_handover_date': DatePickerInput(format='%Y-%m-%d'),
        }


class projectFollow(forms.ModelForm):
    class Meta:
        model = ProjectFollowup
        fields = '__all__'
        exclude = ['project_rep']
        widgets = {
            'followup_remarks': forms.Textarea(attrs={'rows': '5', 'cols': '100'}),
        }
