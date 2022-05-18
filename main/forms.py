from django import forms

class DateForm(forms.Form):
    date_from = forms.SplitDateTimeField(label='Date from')
    date_to = forms.SplitDateTimeField(label='Date to')

