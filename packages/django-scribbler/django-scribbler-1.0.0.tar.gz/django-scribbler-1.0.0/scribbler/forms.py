"Create/edit forms for scribble content."
from django import forms
from django.db.models import ObjectDoesNotExist, FieldDoesNotExist
from django.template import Origin, Template
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text

from .models import Scribble


class ScribbleFormMixin(object):

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if content:
            origin = Origin(content)

            # Try to create a Template
            try:
                template = Template(template_string=force_text(content), origin=origin)
            except Exception as e:
                # This is an error with creating the template
                self.exc_info = {
                    'message': e.args,
                    'line': e.token.lineno,
                    'name': origin.name,
                }
                raise forms.ValidationError('Invalid Django Template')

            # Template has been created; try to parse
            try:
                template.compile_nodelist()
            except Exception as e:
                # This is an error with parsing
                # The data we pass to the views is in e.template_debug
                e.template_debug = template.get_exception_info(e, e.token)
                self.exc_info = e.template_debug
                raise forms.ValidationError('Parsing Error')
        return content


class ScribbleForm(forms.ModelForm, ScribbleFormMixin):

    class Meta(object):
        model = Scribble
        exclude = []
        widgets = {
            'name': forms.HiddenInput,
            'slug': forms.HiddenInput,
            'url': forms.HiddenInput,
        }

    def get_data_prefix(self):
        return self.instance.slug

    def get_preview_url(self):
        content_type = ContentType.objects.get_for_model(Scribble)
        return reverse('preview-scribble', args=(content_type.pk,))

    def get_save_url(self):
        return self.instance.get_save_url()

    def get_delete_url(self):
        return self.instance.get_delete_url()


class PreviewForm(ScribbleForm):

    def clean(self):
        "Override default clean to not check for slug/url uniqueness."
        return self.cleaned_data


class FieldScribbleForm(forms.Form, ScribbleFormMixin):
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, content_type, instance_pk, field_name, *args, **kwargs):
        field_value = kwargs.pop('field_value', None)
        if 'data' not in kwargs:
            kwargs['prefix'] = '{0}:{1}:{2}'.format(content_type.pk, instance_pk, field_name)
        super(FieldScribbleForm, self).__init__(*args, **kwargs)
        self.content_type = content_type
        self.instance_pk = instance_pk
        self.field_name = field_name
        self.fields['content'].initial = field_value
        try:
            self.fields['content'].required = not content_type.model_class()._meta.get_field(field_name).blank
        except FieldDoesNotExist:
            # Error will be caught on form validation
            pass
        self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        if not self.errors:
            ModelClass = self.content_type.model_class()
            try:
                current_instance = ModelClass.objects.get(pk=self.instance_pk)
            except ObjectDoesNotExist as e:
                raise forms.ValidationError(e)
            if not hasattr(current_instance, self.field_name):
                raise forms.ValidationError('{0} model has no field named {1}'.format(
                    ModelClass.__name__, self.field_name))
            setattr(current_instance, self.field_name, self.cleaned_data['content'])
            current_instance.full_clean()
        return self.cleaned_data

    def get_data_prefix(self):
        return self.prefix

    def get_preview_url(self):
        return reverse('preview-scribble', args=(self.content_type.pk,))

    def get_save_url(self):
        args=(self.content_type.pk, self.instance_pk, self.field_name)
        return reverse('edit-scribble-field', args=args)

    def get_delete_url(self):
        raise NotImplementedError()

    def save(self):
        self.content_type.model_class().objects.filter(pk=self.instance_pk).update(
            **{self.field_name: self.cleaned_data.get('content')})
