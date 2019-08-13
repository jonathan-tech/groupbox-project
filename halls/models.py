from django.db import models


class Hall(models.Model):
    title = models.CharField(max_length=250)

class Video(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    #id of a specific video
    youtube_id = models.CharField(max_length=255)
    #his will link the Hall and Video class
    #on_delete-what hapeends if hall gets delted, do we want to delete the videos? yes so we write CASCADE
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
