import requests
from django.shortcuts import render, redirect
from TeachMe.secrets import google_api_key
from ..models import Course, User, Playlist


# course video
def video(request, course_id):
    if "user_id" in request.session:
        logged_user = User.objects.get(id=request.session["user_id"])
        return render(
            request,
            "course_video.html",
            {
                "course": Course.objects.get(id=course_id),
                # "logged_user": User.objects.get(id=request.session["user_id"]),
                "playlists": Playlist.objects.filter(user=logged_user),
            },
        )
    return redirect("/")


def add_to_playlist(request, course_id):
    if request.method == "POST":
        this_user = User.objects.get(id=request.session["user_id"])
        this_playlist = this_user.playlists.get(id=request.POST["playlist"])
        this_playlist.course.add(Course.objects.get(id=course_id))

    if request.POST["hidden"] == "add_to_playlist_and_take_quiz":
        return redirect(f"take_quiz/{course_id}")
    return redirect("/library")


def add_to_new_playlist(request, course_id):
    if request.method == "POST":
        this_user = User.objects.get(id=request.session["user_id"])
        this_playlist = Playlist.objects.create(
            title=request.POST["playlist"], user=this_user
        )
        this_playlist.course.add(Course.objects.get(id=course_id))
    if request.POST["hidden"] == "add_to_playlist_and_take_quiz":
        return redirect(f"take_quiz/{course_id}")
    return redirect("/library")


# course library
def library(request):

    if "user_id" in request.session:
        return render(
            request,
            "course_library.html",
            {"courses": Course.objects.with_questions()},
        )
    return redirect("/")


def library_search(request):
    courses = Course.objects.with_questions()
    if request.POST["search"] != "":
        courses = courses.filter(title__contains=request.POST["search"])

    return render(
        request,
        "library_cards.html",
        {
            "courses": courses,
        },
    )


# profile
def profile(request):
    if "user_id" in request.session:
        logged_user = User.objects.get(id=request.session["user_id"])
        return render(
            request,
            "profile.html",
            {"user": logged_user, "playlists": logged_user.playlists.all()},
        )

    return redirect("/")


# def individual_playlist(request, playlist_id):
#     this_playlist = Playlist.objects.get(id=playlist_id)
#     courses = Course.objects.filter(playlists=this_playlist)

#     score = {}
#     for course in courses:
#         record = course.records.filter(
#             users=User.objects.get(id=request.session["user_id"])
#         )
#         if record:
#             score.update({course.id: record[len(record) - 1].score})

#     return render(
#         request, "individual_playlist.html", {"courses": courses, "scores": score}
#     )


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


# about
def about(request):
    return render(request, "about.html")

def individual_playlist(request, playlist_id):
    this_playlist = Playlist.objects.get(id=playlist_id)
    courses = Course.objects.filter(playlists=this_playlist)

    score = {}
    for course in courses:
        record = course.records.filter(
            users=User.objects.get(id=request.session["user_id"])
        )
        if record:
            score.update({course.id: record[0].score})

    return render(
        request, "individual_playlist.html", {"courses": courses, "scores": score, "playlist": this_playlist}
    )

def delete_playlist(request, playlist_id):
    this_playlist = Playlist.objects.get(id=playlist_id)
    this_playlist.delete()

    return redirect("/profile")
