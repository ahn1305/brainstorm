from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone

from multiselectfield import MultiSelectField
#https://www.youtube.com/watch?v=5jWJBpS0tkg



SPORTS = (
    ('Cricket', 'Cricket'),
    ('Kabadi', 'Kabadi'),
    ('BasketBall', 'Basketball'),
    ('Volleyball', 'Volleyball'),
    ('Hockey', 'Hockey'),
)

MUSIC = (
    ('Rock', 'Rock'),
    ('HipHop', 'HipHop'),
    ('PopMusic', 'PopMusic'),
    ('Instrumental', 'Instrumental'),
    ('Disco', 'Disco'),
)

SCIENCE = (
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('World', 'World'),
    ('Homescience', 'Homescience'),
    ('Purescience', 'Purescience'),
)




class user_interests(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    sports = MultiSelectField(max_length=300, null=True ,choices = SPORTS)
    music = MultiSelectField(max_length=300, null=True, choices = MUSIC)
    science = MultiSelectField(max_length=300, null=True, choices = SCIENCE)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name = 'UserInterests'
    


class Code(models.Model):
    number = models.CharField(max_length=6)

class Survey(models.Model):
    """A survey created by a user."""

    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.title)


class Question(models.Model):
    """A question in a survey"""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=128)

    def __str__(self):
        return(self.prompt)


class Option(models.Model):
    """A multi-choice option available as a part of a survey question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)

    def __str__(self):
        return(self.text)


class Submission(models.Model):
    """A set of answers a survey's questions."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.survey)


class Answer(models.Model):
    """An answer a survey's questions."""

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.option)