from django.db import models

# Create your models here.
from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100)  # A field for the reviewer's name
    rating = models.IntegerField()           # A field for the rating (1-5)
    comment = models.TextField()             # A field for the review comment

    def __str__(self):
        return f'{self.name} - {self.rating}/5'  # This will show the name and rating in the admin interface
