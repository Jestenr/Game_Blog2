from django.urls import path

from .views import *

urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'review/<int:review_id>/',
        review_detail,
        name='review_detail'
    ),

    path(
        'create/',
        create_review,
        name='create_review'
    ),

    path(
        'edit/<int:review_id>/',
        edit_review,
        name='edit_review'
    ),

    path(
        'delete/<int:review_id>/',
        delete_review,
        name='delete_review'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'profile/',
        profile,
        name='profile'
    ),

]