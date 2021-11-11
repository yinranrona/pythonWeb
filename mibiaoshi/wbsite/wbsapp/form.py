from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget=forms.Textarea()
    )

class TimeManageForm(forms.Form):
    taskID = forms.CharField(max_length=50)
    actualStartTime = forms.CharField(max_length=50)
    actualFinishTime = forms.CharField(max_length=50)
