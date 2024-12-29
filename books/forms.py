from django import forms
from books.models import Book, ImageModel
from accounts.models import CustomUser
# for passing label with html tags
from django.utils.safestring import mark_safe

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

CATEGORY_CHOICES = (
   (None, "---Select State---"),
   ("B.Tech.", "B.Tech."),
   ("M.Tech.", "M.Tech."),
   ("MBBS", "MBBS"),
   ("JEE", "JEE"),
   ("NEET PG", "NEET PG"),
   ("NEET UG", "NEET UG"),
   ("NCERT", "NCERT"),
   ("Education", "Education"),
   ("Other", "Other"),
)

asterisk_css = '<span style="color: red; font-weight:bolder;">*</span>'
class BookForm(forms.ModelForm):
    book_name = forms.CharField(label=mark_safe('Book Name'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label=mark_safe('Author'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    edition = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    publication = forms.CharField(label=mark_safe('Publication'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label=mark_safe('Category'+asterisk_css), widget=forms.Select(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(label=mark_safe('Pages'+asterisk_css), min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    seller = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput)
    state = forms.ChoiceField(label=mark_safe('State'+asterisk_css), choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id':'state_id'}))
    city = forms.ChoiceField(label=mark_safe('City'+asterisk_css), choices=[], widget=forms.Select(attrs={'class': 'form-control', 'id':'city_id'}))
    price = forms.IntegerField(label=mark_safe('Price'+asterisk_css), min_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Book
        fields = ['book_name', 'author', 'desc', 'edition', 'publication', 'category', 'pages', 'seller', 'state', 'city', 'price']


class BookImageForm(forms.ModelForm):
  images = forms.ImageField(label="Images*", widget=forms.ClearableFileInput(attrs={"class":"form-control", "id":"images"}))
    
  class Meta:
    model = ImageModel
    fields = ["images"]