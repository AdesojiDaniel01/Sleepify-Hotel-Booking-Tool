from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
