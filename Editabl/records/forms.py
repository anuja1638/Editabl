from sqlite3 import Row
from django import forms


CHOICES = [ ('yes','yes'),
            ('somewhat','somewhat'),
            ('no','no'),]

class feedbackModal(forms.Form):
    radio1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    radio2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    radio3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    feedback = forms.Textarea()