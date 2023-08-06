from django import forms
from django.forms.renderers import TemplatesSetting
from django.forms.utils import pretty_name
from django.utils.safestring import mark_safe

DATE_INPUT_FORMATS = ['%b %d, %Y', '%B %d, %Y']
TIME_INPUT_FORMATS = ['%H:%M %p', '%I:%M %p']
DATETIME_INPUT_FORMATS = ['%b %d, %Y %H:%M %p']


class DateInput(forms.DateInput):
    ATTRS = {'class': 'datepicker'}
    FORMAT = DATE_INPUT_FORMATS

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = self.ATTRS
        if format is None:
            format = self.FORMAT
        super().__init__(attrs=attrs, format=format)


class TimeInput(forms.TimeInput):
    ATTRS = {'class': 'timepicker'}
    FORMAT = TIME_INPUT_FORMATS

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = self.ATTRS
        if format is None:
            format = self.FORMAT
        super().__init__(attrs=attrs, format=format)


class DateTimeInput(forms.DateTimeInput):
    ATTRS = {'class': 'datetimepicker'}
    FORMAT = DATETIME_INPUT_FORMATS

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = self.ATTRS
        if format is None:
            format = self.FORMAT
        super().__init__(attrs=attrs, format=format)


class DateField(forms.DateField):
    input_formats = DATE_INPUT_FORMATS
    widget = DateInput


class TimeField(forms.TimeField):
    input_formats = TIME_INPUT_FORMATS
    widget = TimeInput


class DateTimeField(forms.DateTimeField):
    input_formats = DATETIME_INPUT_FORMATS
    widget = DateTimeInput
    # def __init__(self, *, input_formats=None, **kwargs):
    #     kwargs['widget'] = kwargs.get('widget', DateTimeInput())
    #     super().__init__(input_formats=input_formats, **kwargs)


class CheckboxInput(forms.CheckboxInput):
    template_name = 'materialize_nav/forms/widgets/checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = pretty_name(name)
        return context


class BooleanField(forms.BooleanField):
    widget = CheckboxInput

    def __init__(self, *args, **kwargs):
        kwargs['label'] = kwargs.get('label', False)  # Do not show the label. The input will create the label.
        super().__init__(*args, **kwargs)

