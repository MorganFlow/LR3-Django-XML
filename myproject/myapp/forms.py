from django import forms
from .utils import FIELDS
from .models import Tour

class TourForm(forms.Form):
    storage = forms.ChoiceField(choices=[('xml', 'XML-файл'), ('db', 'База данных')], label='Сохранить в', required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_info in FIELDS.items():
            field_kwargs = {'label': field_info['label'], 'required': field_info['required']}
            if field_info['type'] == str:
                if 'max_length' in field_info:
                    field_kwargs['max_length'] = field_info['max_length']
                if 'choices' in field_info:
                    self.fields[field_name] = forms.ChoiceField(choices=[(c, c) for c in field_info['choices']], **field_kwargs)
                else:
                    self.fields[field_name] = forms.CharField(**field_kwargs)
            elif field_info['type'] == int:
                min_val = field_info.get('min_value')
                self.fields[field_name] = forms.IntegerField(min_value=min_val, **field_kwargs)
            elif field_info['type'] == float:
                min_val = field_info.get('min_value')
                self.fields[field_name] = forms.FloatField(min_value=min_val, **field_kwargs)

class UploadXMLForm(forms.Form):
    file = forms.FileField(label='Загрузить XML-файл')

class TourEditForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'  # Все поля модели