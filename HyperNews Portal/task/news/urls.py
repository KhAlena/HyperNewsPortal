from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("news/create/", views.PostView.as_view()),
    re_path("news/(?P<link>[^/]*)/?/", views.PageView.as_view()),
    path("news/", views.MainPageView.as_view()),
    path("", views.soon),

]


urlpatterns += static(settings.STATIC_URL)
