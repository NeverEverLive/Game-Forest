"""game_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from forum.views import *
from game_forum import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('login/', ForumLogin.as_view(), name='login_page'),
    path('register/', RegisterView.as_view(), name='register_page'),
    path('logout/', LogOutView.as_view(), name='logout_page'),
    # path('detail/<int:pk>', HomeDetailView.as_view(), name='detail_page'),
    path('detail/<int:pk>', detail_page, name='detail_page'),
    path('edit/', edit, name='edit'),
    path('edit_game/', create_game, name='edit_game'),
    path('update_game/<int:pk>', update_game, name='update_game'),
    path('delete_game/<int:pk>', delete_game, name='delete_game'),
    path('edit_company/', create_company, name='edit_company'),
    path('update_company/<int:pk>', update_company, name='update_company'),
    path('delete_company/<int:pk>', delete_company, name='delete_company'),
    path('edit_award/', create_award, name='edit_award'),
    path('update_award/<int:pk>', update_award, name='update_award'),
    path('delete_award/<int:pk>', delete_award, name='delete_award'),

    # path('edit/', GameCreateView.as_view(), name='edit_game'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
