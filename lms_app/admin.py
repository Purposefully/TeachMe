from django.contrib import admin
from .models import User, Playlist, Course, Question, Answer, Topic

admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Topic)
