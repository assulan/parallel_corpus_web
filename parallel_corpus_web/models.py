from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

import datetime

class MyUser(models.Model):
    user = models.OneToOneField(User)
    has_work = models.BooleanField(default=False)

    @property
    def pages(self):
        return [s for s in self.parallelpage_set.all() if not s.is_verified]

    @property
    def num_done(self):
        return len([s for s in self.parallelpage_set.all() if s.is_verified])

    @property
    def num_not_done(self):
        return len([s for s in self.parallelpage_set.all() if not s.is_verified])

    @property
    def num_total(self):
        return len([s for s in self.parallelpage_set.all()])

    def __unicode__(self):
        return self.user.username

class ParallelPage(models.Model):
    file_name = models.TextField()
    kz_text = models.TextField()
    en_text = models.TextField()
    correct_score = models.IntegerField(default=0)
    incorrect_score = models.IntegerField(default=0)
    is_test = models.BooleanField(default=False)
    is_dev = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    my_user = models.ForeignKey(MyUser, blank=True, null=True)
    corpus = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ('sentence', [self.id])

    @property
    def is_verified(self):
        return self.correct_score or self.incorrect_score