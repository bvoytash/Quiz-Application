from django.contrib import admin

from explorebg.questions.models import Question, Answer, Code


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]


class CodeAdmin(admin.ModelAdmin):
    list_display = ('text', 'user')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
# admin.site.register(Like)
admin.site.register(Code, CodeAdmin)
