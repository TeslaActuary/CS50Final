from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('trivia', views.trivia, name='trivia'),
    path('newtrivia', views.newtrivia, name='newtrivia'),
    path('list/<str:venomous>', views.list, name='list'),
    path('<int:snake_id>', views.detail, name='detail'),
    path("create", views.create, name="create"),
]