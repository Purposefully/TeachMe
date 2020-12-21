from django.contrib import admin
from .models import User, Playlist, Course, Question, Answer, Topic
from django.utils.html import format_html
from django.urls import reverse


def linkify(field_name):
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "content",
        "correct_answer_id",
        linkify(field_name="course"),
    ]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = [
        "content",
        linkify(field_name="question"),
        "id",
    ]


admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(Course)
# admin.site.register(Question)
# admin.site.register(Answer)
admin.site.register(Topic)
