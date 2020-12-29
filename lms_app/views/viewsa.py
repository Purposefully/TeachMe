import requests
from django.shortcuts import render, redirect
from TeachMe.secrets import google_api_key
from ..models import Course, User, Topic


def test(request):
    return render(request, "test.html")


# course video
def video(request, course_id):
    if "user_id" in request.session:
        # assumes logging in creates a key named "user_id" in session
        # if request.method == "POST":

        # assumes library page sends post request with course id in a field called "course_id"
        return render(
            request,
            "course_video.html",
            {
                "course": Course.objects.get(id=course_id),
                "logged_user": User.objects.get(id=request.session["user_id"]),
                # "playlist":
            },
        )
    return redirect("/")


def add_to_playlist(request, course_id):

    this_user = User.objects.get(id=request.session["user_id"])
    test_playlist = this_user.playlists.get(id=1)
    test_playlist.course.add(Course.objects.get(id=course_id))
    return redirect(f"/view_here/{course_id}")


# course library
def library(request):
    if "user_id" in request.session:
        return render(
            request,
            "course_library.html",
            {"topics": Topic.objects.all(), "courses": Course.objects.all()},
        )
    return redirect("/")


# profile option
def profile(request, user_id):
    if "user_id" in request.session:
        logged_user = User.objects.get(id=request.session["user_id"])
        return render(
            request,
            "profile.html",
            {"user": logged_user, "playlists": logged_user.playlists.all()},
        )

    return redirect("/")


# def add_playlist():
# logged_user = User.objects.get(id=request.session["user_id"])
# logged_user.playlists.create()

# create a course
def create_course(request):
    if request.method == "POST":

        video_id = request.POST["url"].split("=")[1]

        video_info = requests.get(
            "https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id="
            + video_id
            + "&key="
            + google_api_key
        ).json()

        Course.objects.create(
            title=video_info["items"][0]["snippet"]["title"],
            description=video_info["items"][0]["snippet"]["description"],
            video_id=video_id,
        )

        return redirect("/create_course")
    else:
        return render(request, "create_course.html", {"courses": Course.objects.all()})
