from django import forms

from .models import Review

from .models import Comment


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [

            'game',

            'short_text',

            'full_text',

            'rating'

        ]


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = [

            'text'
            
        ]