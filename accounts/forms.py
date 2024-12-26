from django import forms
from accounts.models import CustomUser

class SignupForm(forms.ModelForm):
    username = forms.CharField(label='Name*', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email*', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password*', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Your Password*', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']
  
    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email*', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password*', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


GENDER_CHOICES = [
    ['M', 'Male'],
    ['F', 'Female'],
    ['O', 'Other']
]
class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Your Name*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.IntegerField(min_value=1000000000, max_value=9999999999, widget=forms.NumberInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label='Gender*', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Photo*', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'mobile', 'gender', 'photo']