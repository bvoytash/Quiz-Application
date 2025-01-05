import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages

from explorebg.questions.forms import CreateQuestionForm, EditQuestionForm, EditAnswerForm
from explorebg.questions.models import Question, Answer, Code

from django.core.mail import send_mail
from django.shortcuts import render
from celery import shared_task
from explorebg.questions.tasks import send_email_task


@login_required
def start_quiz(request):
    if request.method == "POST":
        questions = list(Question.objects.all())
        num_questions = min(len(questions), 10)  # Get up to 10 questions, or fewer if not enough

        if num_questions == 0:
            messages.error(request, "No questions available for the quiz.")
            return render(request, 'quiz/start_quiz.html')

        random_questions = random.sample(questions, num_questions)
        context = {
            'questions': random_questions
        }
        return render(request, 'quiz/play_quiz.html', context)

    return render(request, 'quiz/start_quiz.html')


@login_required
def get_result(request):
    if request.method == "POST":
        dict_qa = {}
        for a in Answer.objects.all():
            if a.correct:
                dict_qa[a.question.text] = a.text

        correct_answers = 0
        for k, v in request.POST.items():
            if dict_qa.get(k) == v:
                correct_answers += 1

        total_questions = len(dict_qa)  # Total questions are the keys in the dictionary
        passed = correct_answers > total_questions / 2  # Compute if more than 50%

        context = {
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'passed': passed  # Add the computed result here
        }
        return render(request, 'quiz/finish_quiz.html', context)


class MyQuestions(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'questions/my_questions.html'
    ordering = ['text']

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


@login_required
def create_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            first_answer = form.cleaned_data['first_answer']
            second_answer = form.cleaned_data['second_answer']
            correct_answer = form.cleaned_data['correct_answer']

            question = Question(
                text=question_text,
                user=request.user,
            )
            question.save()

            answer = Answer(
                text=first_answer,
                correct=False,
                question=question
            )
            answer.save()
            answer = Answer(
                text=second_answer,
                correct=False,
                question=question
            )
            answer.save()
            answer = Answer(
                text=correct_answer,
                correct=True,
                question=question
            )
            answer.save()

            return redirect('my questions')
    else:
        form = CreateQuestionForm()

    context = {
        'form': form,
    }
    return render(request, 'questions/create_question.html', context)


class EditQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'questions/edit.html'
    form_class = EditQuestionForm
    success_url = reverse_lazy('my questions')


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    template_name = 'questions/delete-question.html'
    model = Question
    success_url = reverse_lazy('my questions')


# def like_question(request, pk):
#     question = Question.objects.get(pk=pk)
#     like_object_by_user = question.like_set.filter(user_id=request.user.id).first()
#
#     if like_object_by_user:
#         like_object_by_user.delete()
#     else:
#         like = Like(
#             question=question,
#             user=request.user,
#         )
#         like.save()
#     return redirect('quiz')


class EditAnswerView(LoginRequiredMixin, UpdateView):
    model = Answer
    template_name = 'questions/edit_answer.html'
    form_class = EditAnswerForm
    success_url = reverse_lazy('my questions')


def get_promo_code():
    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    length = 5
    code = "".join(random.sample(symbols, length))
    return code


@login_required
def send_email(request):
    code = get_promo_code()
    user = request.user

    user_email = str(user)
    new_code = Code(
        text=code,
        user=user,
    )
    new_code.save()
                                           # TODO if error: code = get new code

    send_email_task.delay(user_email, code)

    context = {
        'code': code,
    }
    return render(request, 'quiz/send_email.html', context)
