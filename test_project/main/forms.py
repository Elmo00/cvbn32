from django import forms
from django.core.exceptions import ValidationError
import re
import json


class JsonInputDateForm(forms.Form):
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={
        'placeholder': """Валидный формат файла:
[
    {
        "name": "random string less than 50 characters",
        "date": "date string in YYYY-MM-DD_HH:mm format"
    },
    ...
]""",
        'class': 'form-control',
        'rows': 8,
    }))

    @staticmethod
    def valid_format(date: str) -> bool:
        pattern = r"\[[\d\D]+\]"
        if re.fullmatch(pattern, date):
            pattern = r'({[\S\s]+?})'
            for number, peace_of_text in enumerate(re.findall(pattern, date, flags=re.DOTALL), 1):
                pattern_for_name = r'(\s"name":\s?".{1,49}"[,\s]+)'
                pattern_for_data = r'(\s"date":\s?"\d{4}-\d{2}-\d{2}_\d{2}:\d{2}"[\S\s]+?)'
                if not (re.findall(pattern_for_name, peace_of_text) and
                        re.findall(pattern_for_data, peace_of_text)):
                    return False
            else:
                return True
        else:
            return False

    def clean_text(self):
        text = self.cleaned_data['text']
        if not self.valid_format(text):
            raise ValidationError('Форма введенных данных неверна')
        return text
