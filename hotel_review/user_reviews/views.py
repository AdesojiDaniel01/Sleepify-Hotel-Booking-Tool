from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()

    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/review_list.html', context)

