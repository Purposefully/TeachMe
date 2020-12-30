from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("signup", views.signup),
    path("login", views.login),
    path("logout", views.logout),
    path("profile/<int:user_id>", views.profile),
    # path('playlist/<int:playlist_id>', views.get_playlist),
    # path('add_playlist', views.add_playlist),
    path("view_here/<int:course_id>", views.video),
    path("library", views.library),
    path("take_quiz/<int:course_id>", views.take_quiz),
    path("submit_quiz/<int:course_id>", views.take_quiz),
    path("show_quiz_results", views.show_quiz_results),
    path("add_to_playlist/<int:course_id>", views.add_to_playlist),
    path("create_course", views.create_course),
    path("create_quiz", views.create_quiz),
    path("create_random_quiz/<int:course_id>", views.create_random_quiz),
    path("create_real_quiz/<int:course_id>", views.create_real_quiz),
    path("edit_quiz/<int:course_id>", views.edit_quiz),
    # path('grade', views.grade)
    # path('take_quiz/<int:id>', views.get_quiz), (should go to the views where the quiz appears),
    path("video/<int:course_id>", views.video),
    # Dave: this should be used to grab courses from an individual playlist for the profile page
    # path("playlist/<int:playlist_id>", views.individual_playlist)
]
