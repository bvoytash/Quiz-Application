from django import forms

from explorebg.questions.models import Answer, Question


class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        'rows': 4,
    }))
    first_answer = forms.CharField(max_length=200)
    second_answer = forms.CharField(max_length=200)
    correct_answer = forms.CharField(max_length=200)


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }


class EditAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }
