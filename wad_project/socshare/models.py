from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from socshare.utils.models import random_name

class Society(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=15)
    description = models.TextField()
    slug = models.SlugField()
    website = models.URLField(blank=True)
    profile = models.ImageField(upload_to='profile', default='profile/default.jpg')
    banner = models.ImageField(upload_to='profile_banner', default='profile_banner/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.acronym)
        super(Society, self).save(*args, **kwargs)

    def update_banner(self, img):
        '''
        Delete the previous banner and replace with the
        new banner to free up storage space.
        '''
        if self.banner:
            # Make sure it's not the default image
            if not 'default' in self.banner.url:
                self.banner.delete()
        self.banner=img

    def update_profile(self, img):
        if self.profile:
            if not 'default' in self.profile.url:
                self.profile.delete()
        self.profile=img

    class Meta:
        # Fix the table name for admin view
        verbose_name_plural = 'Societies'

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    description_short = models.TextField()
    # Store as "<longitude>, <latitude>"
    location = models.CharField(max_length=30)
    ticket_url = models.URLField()
    views = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='event_banner', default='event_banner/default.png')
    slug = models.SlugField()

    def delete(self, *args, **kwargs):
        '''
        When the model is deleted, we want to remove
        the banned from storage.
        '''
        if self.banner:
            if not 'default' in self.banner.url:
                self.banner.delete()
        super(Event, self).delete(*args, **kwargs)

    def update_banner(self, img):
        if self.banner:
            if not 'default' in self.banner.url:
                self.banner.delete()
        self.banner=img

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_short = self.description[:200]+"..."
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    auth = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Create a random name as comments are anonymous
        self.name = random_name()
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.content[:20]