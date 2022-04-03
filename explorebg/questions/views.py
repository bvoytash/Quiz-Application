import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from explorebg.questions.forms import CreateQuestionForm, EditQuestionForm, EditAnswerForm
from explorebg.questions.models import Question, Answer, Like, PromoCode


@login_required
def start_quiz(request):
    if request.method == "POST":
        questions = [el for el in Question.objects.all()]
        random_questions = random.sample(questions, 2)
        context = {
            'questions': random_questions
        }
        return render(request, 'quiz/play_quiz.html', context)
    return render(request, 'quiz/start_quiz.html')


@login_required
def get_result(request):
    if request.method == "POST":
        answers = [a.text for a in Answer.objects.all() if a.correct]
        correct_answers = 0
        for k, v in request.POST.items():
            print(v)
            if v in answers:
                correct_answers += 1
        context = {
            'correct_answers': correct_answers
        }
        return render(request, 'quiz/finish_quiz.html', context)


# @login_required
# def get_quiz(request):
#     questions = Question.objects.all()
#     user = request.user
#     # r_questions = random.sample(list(questions), 2)
#     is_liked = {}
#     for q in questions:
#         if q.like_set.filter(user_id=request.user.id).first():
#             is_liked[q.text] = True
#         else:
#             is_liked[q.text] = False
#
#     if request.method == 'POST':
#         correct_answers = 0
#         for question in questions:
#             answer = [answer.text for answer in question.get_answer() if answer.correct][0]
#             if request.POST.get(question.text) == answer:
#                 correct_answers += 1
#         print(correct_answers)
#         context = {
#             'correct_answers': correct_answers,
#             'user': user,
#         }
#
#         return render(request, 'finish_quiz.html', context)
#
#     context = {
#         'questions': questions,
#         'user': user,
#         'is_liked': is_liked,
#     }
#     return render(request, 'questions.html', context)


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


#
# class LikeQuestionView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         question = Question.objects.get(pk=self.kwargs['pk'])
#         like_object_by_user = question.like_set.filter(user_id=self.request.user.id) \
#             .first()
#         if like_object_by_user:
#             like_object_by_user.delete()
#         else:
#             like = Like(
#                 question=question,
#                 user=self.request.user,
#             )
#             like.save()
#         return redirect('quiz')

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
    length = 4
    code = "".join(random.sample(symbols, length))
    return code


@login_required
def send_email(request):
    code = get_promo_code()
    user = request.user
    new_code = PromoCode(
        text=code,
        user=user,
    )
    new_code.save()
    send_mail('Hello from Explore Quiz',
              f"Your code is {code}",
              'explore-quiz@abv.bg',
              [f'{user}'],
              fail_silently=False)

    context = {
        'code': code,
    }
    return render(request, 'quiz/send_email.html', context)
