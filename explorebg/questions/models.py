import random

from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Question(models.Model):
    text = models.CharField(max_length=500)

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def get_answer_quiz(self):
        answers = [ans for ans in self.answer_set.all()]
        random.shuffle(answers)
        return answers

    def get_answer(self):
        return self.answer_set.all()

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text} answer: {self.text}, correct: {self.correct}"


class Like(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class PromoCode(models.Model):
    text = models.CharField(max_length=4)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
