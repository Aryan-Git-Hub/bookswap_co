from django import forms
from books.models import Book
from accounts.models import CustomUser

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
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    colony = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Book
        fields = ['book_name', 'author', 'desc', 'edition', 'publication', 'category', 'pages', 'photo', 'seller', 'state', 'city', 'colony']