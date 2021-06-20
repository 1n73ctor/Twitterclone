from django import forms

from .models import Tweet

MAX_TWEET_LEN = 10

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LEN:
            raise forms.ValidationError("Oh you Exceed max len")
        return content