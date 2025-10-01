from django import forms

class BookForm(forms.Form):
    author = forms.CharField(label='Author Name', max_length=100)
    title = forms.CharField(label='Book Title', max_length=100)
    pages = forms.IntegerField(label='Number of Pages')
    year = forms.IntegerField(label='Year of Publication')