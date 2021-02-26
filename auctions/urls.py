from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlist", views.newlist, name="newlist"),
    path("details/<int:pk>", views.details, name="details"),
    path("watchlist/<int:product_id>", views.addwatchlist, name="addwatchlist"),
    path("remove/<int:watchlist_id>", views.remove, name="remove"),
    path("watchlist", views.watch, name ="watchlist"),
    path("comment/<int:pk>", views.comment, name="comments"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),

]
