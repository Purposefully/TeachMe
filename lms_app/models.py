from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name must be at least 2 characters long."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email address is invalid."
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors["pwd_match"] = "Password must match Re-type Password"
        return errors


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

    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name="playlists", on_delete = models.CASCADE)
    course = models.ManytoMany(Course, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class User_Quiz_Record(models.Model):
    users = models.ManyToManyField(User, related_name="records")
    course = models.ManyToManyField(Course, related_name="records")
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    content = models.TextField()
    correct_answer_id = models.IntegerField()
    course = models.ForeignKey(Course, related_name="questions", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Answer(models.Model):
    content = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name="answers", on_delete = models.CASCADE)
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