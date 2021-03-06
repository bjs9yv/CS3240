from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.contrib.auth.models import Group
from .models import Folder, Report, File

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

"""class ReportForm(forms.Form):
    report_description = forms.CharField(label='Description', max_length=80, required=True)
    report_keyword = forms.CharField(label='Keyword', max_length=15,required=False)
    report_body = forms.CharField(widget=forms.Textarea, label='Type your report here')
    report_files = MultiFileField()
    report_is_private = forms.BooleanField(widget=widgets.CheckboxInput, label='Private', required=False)
    report_is_encrypted = forms.BooleanField(widget=widgets.CheckboxInput, label='Encrypted', required=False)
    report_folder = forms.ModelChoiceField(queryset=Folder.objects.all(), label='Folder', required=False)
    """

class ReportForm(forms.ModelForm):
    files = MultiFileField()

    class Meta:
        model = Report
        fields = ('description', 'keyword', 'text', 'folder', 'private', 'encrypted', 'group')
        widgets = {
                'description': None,
                'keyword': None,
            }

    def __init__(self, user, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user)
        self.fields['group'].queryset = user.groups.all()
        self.instance.owner = user

    def save_files(self):
        for f in self.cleaned_data['files']:
            File(file=f, attached_to=self.instance).save()

    def save(self, commit=True):
        r = super(ReportForm, self).save(commit=commit)
        if commit:
            self.save_files()
        else:
            raise Exception('how to m2m')
        return r

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name', 'parent')

    def __init__(self, user, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Folder.objects.filter(owner=user)
        self.user = user

    def save(self, commit=True):
        f = super(FolderForm, self).save(commit=False)
        f.owner = self.user
        if commit:
            f.save()
        return f
    
class GroupForm(forms.ModelForm):
    name = forms.CharField(label='Group name', max_length=50)

    class Meta:
        model = Group
        fields = ('name',)

class AddUserToGroupForm(forms.Form):
    username = forms.CharField(label='Username')

class SiteManagerForm(forms.Form):
    username = forms.CharField(label='Username')
    group = forms.CharField(label='Group', required=False)
