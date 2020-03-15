from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

class Society(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=15)
    slug = models.SlugField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.acronym)
        super(Society, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Societies'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    location = models.CharField(max_length=30)
    ticket_url = models.URLField()
    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]