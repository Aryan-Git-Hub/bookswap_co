from django import forms
from accounts.models import CustomUser, Address
# for passing label with html tags
from django.utils.safestring import mark_safe
# to change password
from django.core.validators import RegexValidator


asterisk_css = '<span style="color: red; font-weight:bolder;">*</span>'

class SignupForm(forms.ModelForm):
    username = forms.CharField(label=mark_safe('Name'+asterisk_css), max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id':'username', 'placeholder': ' '}))
    email = forms.EmailField(label=mark_safe('Email'+asterisk_css), max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder': ' '}))
    password = forms.CharField(label=mark_safe("Password"+asterisk_css),
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password', 'placeholder': ' '}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._])[A-Za-z\d@$!%*?&._]{8,}$',
                message=(
                    "Password must be at least 8 characters long, "
                    "contain at least one uppercase letter, one number, "
                    "and one special character."
                ),
                code='invalid_password'
            ),
        ]
    )
    confirm_password = forms.CharField(label=mark_safe('Confirm Password'+asterisk_css), max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'confirmPassword', 'placeholder': ' '}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']
  
    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


class LoginForm(forms.Form):
    email = forms.EmailField(label=mark_safe('Enter your email'+asterisk_css), max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'email', 'placeholder': ' '}))
    password = forms.CharField(label=mark_safe('Enter your password'+asterisk_css), max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'password', 'placeholder': ' '}))
    
    class Meta:
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


GENDER_CHOICES = [
    [None, '---Select Gender---'],
    ['M', 'Male'],
    ['F', 'Female'],
    ['O', 'Other']
]


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label=mark_safe('Your Name'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.IntegerField(label=mark_safe('Mobile'+asterisk_css), min_value=1000000000, max_value=9999999999, widget=forms.NumberInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label=mark_safe('Gender'+asterisk_css), choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label=mark_safe('Photo'+asterisk_css), widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'mobile', 'gender', 'photo']



STATE_CHOICES = [
  [None, "---Select State---"],
  ["Andaman and Nicobar Islands", "Andaman and Nicobar Islands"],
  ["Andhra Pradesh", "Andhra Pradesh"],
  ["Arunachal Pradesh", "Arunachal Pradesh"],
  ["Assam", "Assam"],
  ["Bihar", "Bihar"],
  ["Chandigarh", "Chandigarh"],
  ["Chhattisgarh", "Chhattisgarh"],
  ["Dadra and Nagar Haveli", "Dadra and Nagar Haveli"],
  ["Daman and Diu", "Daman and Diu"],
  ["Delhi", "Delhi"],
  ["Goa", "Goa"],
  ["Gujarat", "Gujarat"],
  ["Haryana", "Haryana"],
  ["Himachal Pradesh", "Himachal Pradesh"],
  ["Jammu and Kashmir", "Jammu and Kashmir"],
  ["Jharkhand", "Jharkhand"],
  ["Karnataka", "Karnataka"],
  ["Kerala", "Kerala"],
  ["Ladakh", "Ladakh"],
  ["Lakshadweep", "Lakshadweep"],
  ["Madhya Pradesh", "Madhya Pradesh"],
  ["Maharashtra", "Maharashtra"],
  ["Manipur", "Manipur"],
  ["Meghalaya", "Meghalaya"],
  ["Mizoram", "Mizoram"],
  ["Nagaland", "Nagaland"],
  ["Narora", "Narora"],
  ["Odisha", "Odisha"],
  ["Pondicherry", "Pondicherry"],
  ["Punjab", "Punjab"],
  ["Rajasthan", "Rajasthan"],
  ["Sikkim", "Sikkim"],
  ["Tamil Nadu", "Tamil Nadu"],
  ["Telangana", "Telangana"],
  ["Tripura", "Tripura"],
  ["Uttar Pradesh", "Uttar Pradesh"],
  ["Uttarakhand", "Uttarakhand"],
  ["West Bengal", "West Bengal"]
]

class AddressForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput)
    pincode = forms.IntegerField(label=mark_safe("Pincode"+asterisk_css), min_value=100000, max_value=999999, widget=forms.NumberInput(attrs={'class':'form-control'}))
    mobile = forms.IntegerField(label=mark_safe("Mobile"+asterisk_css), min_value=1000000000, max_value=9999999999, widget=forms.NumberInput(attrs={'class':'form-control'}))
    state = forms.ChoiceField(label=mark_safe('State'+asterisk_css), choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id':'state_id'}))
    city = forms.ChoiceField(label=mark_safe('City'+asterisk_css), choices=[], widget=forms.Select(attrs={'class': 'form-control', 'id':'city_id'}))
    class Meta:
        model = Address
        fields = ['user', 'full_name', 'mobile', 'pincode', 'state', 'city', 'full_address', 'some_instructions']
        labels = {
            "full_name": mark_safe("Full Name"+asterisk_css),
            "full_address": mark_safe("Full Address"+asterisk_css),
            "some_instructions": "Some Instructions",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={'class':'form-control', 'id':'full_name', 'placeholder': ' '}),
            "full_address": forms.Textarea(attrs={'class':'form-control', 'placeholder': ' '}),
            "some_instructions": forms.Textarea(attrs={'class':'form-control', 'placeholder': ' '})
        }



class OtpForm(forms.Form):
    otp = forms.IntegerField(label="Enter OTP: ", min_value=100000, max_value=999999, widget=forms.NumberInput(attrs={'class':'form-control'}))

    
class ChangePassword(forms.Form):
    email = forms.EmailField(label="Email: ", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label="New Password: ",
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._])[A-Za-z\d@$!%*?&._]{8,}$',
                message=(
                    "Password must be at least 8 characters long, "
                    "contain at least one uppercase letter, one number, "
                    "and one special character."
                ),
                code='invalid_password'
            ),
        ]
    )