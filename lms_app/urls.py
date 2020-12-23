from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("signup", views.signup),
    path("login", views.login),
    path("profile", views.profile),
    # path('playlist/<int:playlist_id>', views.get_playlist),
    # path('add_playlist', views.add_playlist),
    path("view_here/<int:course_id>", views.video),
    path("library", views.library),
    path("take_quiz/<int:course_id>", views.get_quiz),
    # path('add_to_playlist/<int:course_id>', views.add_to_playlist),
    path("create_course", views.create_course),
    # path('test', views.test),
    # path('Lisa', views.Lisa),
    # path('grade', views.grade)
    # path('take_quiz/<int:id>', views.get_quiz), (should go to the views where the quiz appears),
    path("video/<int:course_id>", views.video),
]
