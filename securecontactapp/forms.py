from django import forms

class MessageForm(forms.Form):
    message_recipient = forms.CharField(max_length=30)
    message_body = forms.TextField(label='Type your message here')
    
class ReportForm(forms.Form):
    report_body = forms.TextField(label='Type your report here')

class FolderForm