from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("signup", views.signup),
    path("login", views.login),
    path("logout", views.logout),
    path("profile", views.profile),
    path("about", views.about),
    # path('playlist/<int:playlist_id>', views.get_playlist),
    # path('add_playlist', views.add_playlist),
    #Look at one specific video
    path("view_here/<int:course_id>", views.video),
    #Library views
    path("library-search/", views.library_search),
    path("library", views.library),
    #Take quiz from the course video page (without taking course)
    path("take_quiz/<int:course_id>", views.take_quiz),
    path("submit_quiz/<int:course_id>", views.take_quiz),
    path("show_quiz_results", views.show_quiz_results),
    #Add to playlist from individual quiz page
    path("add_to_playlist/<int:course_id>", views.add_to_playlist),
    path("add_to_new_playlist/<int:course_id>", views.add_to_new_playlist),
    path("create_course", views.create_course),
    path("manage_quizzes", views.manage_quizzes),
    path("create_random_quiz/<int:course_id>", views.create_random_quiz),
    path("create_real_quiz/<int:course_id>", views.create_real_quiz),
    path("edit_quiz/<int:course_id>", views.edit_quiz),
    # path('grade', views.grade)
    # path('take_quiz/<int:id>', views.get_quiz), (should go to the views where the quiz appears),
    path("video/<int:course_id>", views.video),
    # Dave: this should be used to grab courses from an individual playlist for the profile page
    # path("playlist/<int:playlist_id>", views.individual_playlist)
]
