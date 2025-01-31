from django.shortcuts import render
from .models import Review

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'hotel_reviews/review_list.html', {'reviews': reviews})
