from .models import Video
from django import forms

class VideoForm(forms.ModelForm):
    '''
    pass me a model and ill create
    a form
    '''
    class Meta:
        model=Video
        fields = ['title','url','youtube_id']

class SearchForm(forms.Form):
    '''
    this will make a regualr djano forms
    '''
    search_term = forms.CharField(max_length = 255, label ='Search for Video:')
