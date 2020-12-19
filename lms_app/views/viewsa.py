from django.shortcuts import render, redirect
from ..models import Course, User, Topic


def test(request):
    return render(request, "test.html")


# course video
def video(request):
    if "user_id" in request.session:
        # assumes logging in creates a key named "user_id" in session
        if request.method == "POST":
            # assumes library page sends post request with course id in a field called "course_id"
            return render(
                request,
                "course_video.html",
                {
                    "Course": Course.objects.get(id=request.POST["course_id"]),
                    "logged_user": User.objects.get(id=request.session["user_id"]),
                },
            )
    return redirect("/")


# course library
def library(request):
    if "user_id" in request.session:
        # assuming library template called "course_library"
        return render(request, "course_library.html", {"topics": Topic.objects.all()})
    return redirect("/")


# profile option
def profile(request):
    if "user_id" in request.session:

        # assuming profile template is called "profile_option"
        return render(
            request,
            "profile_option.html",
            {"logged_user": User.objects.get(id=request.session["user_id"])},
        )

    return redirect("/")


# def add_playlist():
#   logged_user = User.objects.get(id=request.session["user_id"])
#  logged_user.playlists.create()
