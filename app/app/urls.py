"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from users.views.customers import CustomerWaitListView 
from core.views.custom_user import HomePageView, AboutPageView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('incidents/', include('incidents.urls',)),
    #path('', include('users.urls')),
   # path('signup/', CustomUserSignUpView.as_view(), name='signup'),
    #path('signup/customers', CustomerWaitListView.as_view(), name='signup_customer'),
    #path('', HomePageView.as_view(), name='home'),
    #path('about/', AboutPageView.as_view(), name='about'),
    #path('', include('waitinglist.urls'), name='waitinglist'),
    #path('', include('cohorts.urls'), name='cohorts'),
    
    
]
