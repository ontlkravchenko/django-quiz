from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
    # path("register", views.register_view, name="register"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("create_quiz", views.create_quiz, name="create_quiz"),
    # path("leaderboard", views.leaderboard, name="leaderboard"),
    # path("profile_page/<int:userId>", views.profile_page, name="profile_page"),

    # # API routes
    # path("api/check_answer", views.check_answer, name="check_answer"),
    # path("api/change_score", views.change_score, name="change_score"),
    # path("api/generate_quiz", views.generate_quiz, name="generate_quiz"),
    # path("api/create_quiz_api", views.create_quiz_api, name="create_quiz_api")
]
