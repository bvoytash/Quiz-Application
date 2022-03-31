from django.urls import path

from explorebg.questions.views import create_question, MyQuestions, \
    EditAnswerView, DeleteQuestionView, send_email, start_quiz, get_result, EditQuestionView

urlpatterns = [
    # path('', get_quiz, name='quiz'),
    path('create/', create_question, name='create question'),
    path('my-questions/', MyQuestions.as_view(), name='my questions'),
    path('edit/<int:pk>', EditQuestionView.as_view(), name='edit question'),
    path('delete/<int:pk>', DeleteQuestionView.as_view(), name='delete question'),
    # path('like/<int:pk>', like_question, name='like question'),
    path('edit/answer/<int:pk>', EditAnswerView.as_view(), name='edit answer'),
    path('send-mail/', send_email, name='send email'),

    path('start/', start_quiz, name='start quiz'),
    path('get-result/', get_result, name='get result'),
]
