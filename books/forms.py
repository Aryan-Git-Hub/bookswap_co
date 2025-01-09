from django import forms
from books.models import Book, ImageModel
from accounts.models import CustomUser
# for passing label with html tags
from django.utils.safestring import mark_safe


CATEGORY_CHOICES = [
    [None, "---Select Category---"],
    ['Fiction', 'Fiction'], 
    ['Non-Fiction', 'Non-Fiction'],
    ["Children's Books", "Children's Books"],
    ['Young Adult (YA)', 'Young Adult (YA)'], 
    ['Educational', 'Educational'], 
    ['Comics & Graphic Novels', 'Comics & Graphic Novels'], 
    ['Poetry', 'Poetry'], 
    ['Religion & Spirituality', 'Religion & Spirituality'], 
    ['Science & Nature', 'Science & Nature'], 
    ['Self-Improvement', 'Self-Improvement'], 
    ['Art & Photography', 'Art & Photography'], 
    ['Travel & Adventure', 'Travel & Adventure'], 
    ['Cooking & Food', 'Cooking & Food'], 
    ['Sports & Outdoors', 'Sports & Outdoors'], 
    ['Fantasy', 'Fantasy'], 
    ['Science Fiction', 'Science Fiction'], 
    ['School Education', 'School Education'], 
    ['Competitive Exams', 'Competitive Exams'], 
    ['Undergraduate Courses', 'Undergraduate Courses'], 
    ['Postgraduate Courses', 'Postgraduate Courses'], 
    ['Vocational and Skill Development', 'Vocational and Skill Development'], 
    ['Entrance Exam Preparation', 'Entrance Exam Preparation'], 
    ['School Subjects by Stream', 'School Subjects by Stream'], 
    ['Technology and Professional Studies', 'Technology and Professional Studies'], 
    ['Medical and Healthcare', 'Medical and Healthcare'],
    ['Others', 'Others']
    ]

asterisk_css = '<span style="color: red; font-weight:bolder;">*</span>'
class BookForm(forms.ModelForm):
    book_name = forms.CharField(label=mark_safe('Book Name'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label=mark_safe('Author'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    edition = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    publication = forms.CharField(label=mark_safe('Publication'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label=mark_safe('Category'+asterisk_css), widget=forms.Select(attrs={'class': 'form-control'}))
    sub_category = forms.ChoiceField(choices=((None, "---Select Sub-Category---"),), label=mark_safe('Sub Category'+asterisk_css), widget=forms.Select(attrs={'class': 'form-control', 'id':'id_sub_category'}))
    pages = forms.IntegerField(label=mark_safe('Pages'+asterisk_css), min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    seller = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput)
    selected_address_id = forms.ChoiceField(widget=forms.RadioSelect)
    price = forms.IntegerField(label=mark_safe('Price'+asterisk_css), min_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Book
        fields = ['book_name', 'author', 'desc', 'edition', 'publication', 'category', 'sub_category', 'pages', 'seller', 'price', 'selected_address_id']


class BookImageForm(forms.ModelForm):
  images = forms.ImageField(label="Images*", widget=forms.ClearableFileInput(attrs={"class":"form-control", "id":"images"}))
    
  class Meta:
    model = ImageModel
    fields = ["images"]


class BookAdEditForm(forms.ModelForm):
    book_name = forms.CharField(label=mark_safe('Book Name'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label=mark_safe('Author'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='Description', max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    edition = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    publication = forms.CharField(label=mark_safe('Publication'+asterisk_css), max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pages = forms.IntegerField(label=mark_safe('Pages'+asterisk_css), min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label=mark_safe('Price'+asterisk_css), min_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Book
        fields = ['book_name', 'author', 'desc', 'edition', 'publication', 'pages', 'price']