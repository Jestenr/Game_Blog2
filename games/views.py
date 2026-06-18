from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .models import (
    Review,
    Game
)

from .forms import ReviewForm

from .models import Comment
from .forms import CommentForm

from django.contrib.auth.models import User


def home(request):

    reviews = Review.objects.filter(
        approved=True
    ).order_by('-created_at')

    search = request.GET.get('search')

    if search:

        reviews = reviews.filter(

            Q(game__title__icontains=search)

            |

            Q(short_text__icontains=search)

            |

            Q(full_text__icontains=search)

        )

    top_games = Game.objects.order_by(
        '-average_rating'
    )[:5]

    users_count = User.objects.count()

    reviews_count = Review.objects.count()

    games_count = Game.objects.count()

    return render(
    request,
    'games/home.html',
    {
        'reviews': reviews,
        'top_games': top_games,

        'users_count': users_count,
        'reviews_count': reviews_count,
        'games_count': games_count,
    }
)


def review_detail(
        request,
        review_id
):

    review = Review.objects.get(
        id=review_id
    )

    comments = Comment.objects.filter(
        review=review
    ).order_by('-created_at')

    form = CommentForm()

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = CommentForm(
                request.POST
            )

            if form.is_valid():

                comment = form.save(
                    commit=False
                )

                comment.review = review

                comment.author = request.user

                comment.save()

                return redirect(
                    f'/review/{review.id}/'
                )

    return render(
        request,
        'games/review_detail.html',
        {
            'review': review,
            'comments': comments,
            'form': form
        }
    )

def create_review(request):

    if not request.user.is_authenticated:

        return redirect('login')

    form = ReviewForm()

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.author = request.user

            review.save()

            review.game.update_rating()

            return redirect('/')

    return render(
        request,
        'games/review_create.html',
        {
            'form': form
        }
    )


def edit_review(
        request,
        review_id
):

    review = Review.objects.get(
        id=review_id
    )

    if (
        request.user != review.author
        and
        not request.user.is_superuser
    ):
        return HttpResponseForbidden()

    form = ReviewForm(
        instance=review
    )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            review = form.save()

            review.game.update_rating()

            return redirect('/')

    return render(
        request,
        'games/review_create.html',
        {
            'form': form
        }
    )


def delete_review(
        request,
        review_id
):

    review = Review.objects.get(
        id=review_id
    )

    if (
        request.user != review.author
        and
        not request.user.is_superuser
    ):
        return HttpResponseForbidden()

    game = review.game

    review.delete()

    game.update_rating()

    return redirect('/')


def register(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.is_active = False

        user.save()

        return redirect('/login')

    return render(
        request,
        'games/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect('/')

    return render(
        request,
        'games/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('/')

def profile(request):

    reviews = Review.objects.filter(
        author=request.user
    )

    return render(
        request,
        'games/profile.html',
        {
            'reviews': reviews
        }
    )

