from django.contrib import admin
from .models import User, Playlist, Course, Question, Answer, Topic, UserQuizRecord
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
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = [
        "title",
        "description",
        # linkify(field_name="question"),
        "video_id",
    ]

@admin.register(UserQuizRecord)
class UserQuizRecordAdmin(admin.ModelAdmin):

    readonly_fields = ('id',)

    list_display = [
        "get_user",
        "get_course",
        # linkify(field_name="users"),
        # linkify(field_name="course"),
        "score",
        "id",
    ]

    def get_course(self, obj):
        return "\n".join([x.title for x in obj.course.all()])

    def get_user(self, obj):
        return "\n".join([x.name for x in obj.users.all()])

admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(Topic)
