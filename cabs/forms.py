from django import forms
from . import models


class CreatePost(forms.ModelForm):
    class Meta:
        model=models.Post
        fields=('passengers','time','pickup_from','destination','date','gender')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        exclude = []