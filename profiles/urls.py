from django.urls import path

from profiles.views import ProfileView

urlpatterns = [
    # URL для действий с профилем пользователя
    path("", ProfileView.as_view()),
]
