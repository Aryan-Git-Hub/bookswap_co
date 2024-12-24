from django import forms
from books.models import Book

class BookForm(forms.ModelForm):
    book_name = forms.CharField(label='Book Name*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label='Author*', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='Description*', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
    edition = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    publication = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    category = forms.CharField(label='Category*', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(required=False)
    photo = forms.ImageField()