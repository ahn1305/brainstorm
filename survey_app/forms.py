from django.forms import ModelForm
from django import forms
from .models import user_interests,Code,Survey, Question, Option



class UserInterestsForm(ModelForm):
	class Meta:
		model = user_interests
		fields = ['sports','music','science'] # order of the form
		
class CodeForm(forms.ModelForm):
	number = forms.CharField(

		label='Code',
		help_text='',
		widget=forms.TextInput(attrs={'placeholder': 'Otp will be sent to your email'}),

		)
	
	class Meta:
		model = Code
		fields = ('number',)
	
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["prompt"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = {(o.pk, o.text) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs