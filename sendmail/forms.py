from django import forms
from django.forms import DateTimeInput

from sendmail.models import Mailing


class MailingCreateForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('next_date', 'owner',)

    widgets = {
        'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
