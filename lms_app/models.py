import re
from django.db import models

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data["name"]) < 2:
            errors["name"] = "Name must be at least 2 characters long."
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["email"] = "Email address is invalid."
        if len(post_data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        if post_data["password"] != post_data["confirm_password"]:
            errors["pwd_match"] = "Password must match Re-type Password"
        return errors


class CourseManager(models.Manager):
    def with_questions(self):
        # Get all questions from current quizzes
        questions = Question.objects.all()
        # Create list for ids of courses that have quizzes
        courses_with_questions = []
        # For each question, get the related course id and add to list
        for question in questions:
            if question.course.id not in courses_with_questions:
                courses_with_questions.append(question.course.id)
        # Return all courses for those that have quizzes
        return Course.objects.filter(id__in=courses_with_questions)


class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # This provides a name for when looking at the database from admin view (superuser)
    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_id = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name="playlists", on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserQuizRecord(models.Model):
    users = models.ManyToManyField(User, related_name="records")
    course = models.ManyToManyField(Course, related_name="records")
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Question(models.Model):
    content = models.TextField()
    correct_answer_id = models.IntegerField()
    course = models.ForeignKey(
        Course, related_name="questions", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Topic(models.Model):
    title = models.CharField(max_length=45)
    courses = models.ManyToManyField(Course, related_name="topics")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
