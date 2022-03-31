from django.contrib import admin

from explorebg.questions.models import Question, Answer, PromoCode


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('text', 'user')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
# admin.site.register(Like)
admin.site.register(PromoCode, PromoCodeAdmin)
