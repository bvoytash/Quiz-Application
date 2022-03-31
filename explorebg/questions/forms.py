from django import forms

from explorebg.questions.models import Answer, Question


class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        'rows': 4,
        'size': '30',
        'style': 'border: solid; border-color:green; border-radius: 10px; font-size: 0.8rem;' 'font: bold;',
    }))
    first_answer = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'size': '30',
        'style': 'border: solid;; border-color:green; border-radius: 10px; font-size: 1rem;'
    }))
    second_answer = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'size': '30',
        'style': 'border: solid;; border-color:green; border-radius: 10px; font-size: 1rem;'
    }))
    correct_answer = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'size': '30',
        'style': 'border: solid;; border-color:green; border-radius: 10px; font-size: 1rem;'
    }))


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'asd',
                    'size': '35',
                    'style': 'border: solid; border-color:green; border-radius: 10px; font-size: 120%;' 'font: bold;',
                }
            )
        }


class EditAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 2,
                    'class': 'asd',
                    'size': '35',
                    'style': 'border: solid; border-color:green; border-radius: 10px; font-size: 120%;' 'font: bold;',
                }
            ),
        }
