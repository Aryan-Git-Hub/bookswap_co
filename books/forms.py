from django import forms
from books.models import Book
from accounts.models import CustomUser

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


class BookForm(forms.ModelForm):
    book_name = forms.CharField(label='Book Name*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label='Author*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    edition = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    publication = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    category = forms.CharField(label='Category*', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Photo*', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    seller = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput)
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id':'state_id'}))
    city = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control', 'id':'city_id'}))

    class Meta:
        model = Book
        fields = ['book_name', 'author', 'desc', 'edition', 'publication', 'category', 'pages', 'photo', 'seller', 'state', 'city']