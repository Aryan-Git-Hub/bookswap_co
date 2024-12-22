from django import forms
from accounts.models import CustomUser

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Your Name*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your Email*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Gender*', choices=CustomUser.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'gender']