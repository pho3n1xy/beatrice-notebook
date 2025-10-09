"""
URL configuration for beatricenotebook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from journal import views as journal_views

urlpatterns = [
    path('', journal_views.homepage_router_view, name='homepage_router'),

    path('admin/', admin.site.urls),

    # This line tells the project: "For any URL that starts with 'journal/',
    # hand off the rest of the URL to be handled by the 'journal.urls' file."
    path('journal/', include('journal.urls', namespace='journal')),

    #paths for login and logout below
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
