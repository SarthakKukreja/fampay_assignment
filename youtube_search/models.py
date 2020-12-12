from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    date_published = models.DateTimeField()
    thumbnail_url = models.TextField(null=True)
    video_id = models.CharField(max_length=15 , unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date_published',)

class VariableStorage(models.Model):
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
