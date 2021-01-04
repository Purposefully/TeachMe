import requests
from django.shortcuts import render, redirect
from TeachMe.secrets import google_api_key
from ..models import Course, User, Topic, Playlist, Question


def test(request):
    return render(request, "test.html")


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
        # Note: added by Lisa.  Feel free to discard or improve
        # If admin has added a course but not created a quiz,
        # I'm assuming we wouldn't want the course showing up in the library yet?
        # Therefore, this pulls only courses that have quizzes

        # Get all questions from current quizzes
        questions = Question.objects.all()
        # Create list for ids of courses that have quizzes
        courses_with_questions = []
        # For each question, get the related course id and add to list
        for question in questions:
            if question.course.id not in courses_with_questions:
                courses_with_questions.append(question.course.id)

        # Filter all courses for those that have quizzes
        courses_to_display = Course.objects.filter(id__in=courses_with_questions)

        return render(
            request,
            "course_library.html",
            {"courses": courses_to_display},
        )
    return redirect("/")


def library_search(request):
    return render(
        request,
        "course_library.html",
        {
            "courses": Course.objects.filter(title__contains=request.GET["search"]),
        },
    )


# profile option
def profile(request):
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


# about
def about(request):
    return render(request, "about.html")


def individual_playlist(request, playlist_id):
    this_playlist = Playlist.objects.get(id=playlist_id)
    context = {"courses": Course.objects.filter(playlists=this_playlist)}
    return render(request, "individual_playlist.html", context)
