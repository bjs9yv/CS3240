from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import widgets

# From http://koensblog.eu/blog/7/multiple-file-upload-django/
class MultiFileInput(forms.FileInput):
    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]

# From http://koensblog.eu/blog/7/multiple-file-upload-django/
class MultiFileField(forms.FileField):
    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size' : u"File: %(uploaded_file_name)s, exceeded maximum upload size."
    }
    
    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
        elif self.max_num and  num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
        for uploaded_file in data:
            if self.maximum_file_size != None and uploaded_file.size > self.maximum_file_size:
                raise ValidationError(self.error_messages['file_size'] % { 'uploaded_file_name': uploaded_file.name})

        return True

class MessageForm(forms.Form):
    message_recipient = forms.CharField(label='Send to', max_length=30)
    message_body = forms.CharField(widget=forms.Textarea, label='Type your message here')
    encrypted = forms.BooleanField(widget=widgets.CheckboxInput, label='Encrypt this message?', required=False)

class ReportForm(forms.Form):
    report_body = forms.CharField(widget=forms.Textarea, label='Type your report here')
    report_files = MultiFileField()

class FolderForm(forms.Form):
    # Should have auto-generated primary keys since names aren't unique among users
    username = forms.CharField(label='Username')
    # Reports need to have a "folder" foreign key field
    
class GroupForm(forms.Form):
    group_name = forms.CharField(label='Group name', max_length=50)
    group_is_private = forms.BooleanField(widget=widgets.CheckboxInput, label='Hidden', required=False)
    group_members_can_invite = forms.BooleanField(widget=widgets.CheckboxInput, label='Members can invite', required=False)

class SiteManagerForm(forms.Form):
    username = forms.CharField(label='Username')
