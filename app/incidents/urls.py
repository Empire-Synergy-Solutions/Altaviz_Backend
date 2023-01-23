from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView
from .views import home

urlpatterns = (
    [
        #path("", TemplateView.as_view(template_name="home.html"), name="home"),
        path("", home.dashboard_functions, name="home"),
        path("profile", TemplateView.as_view(template_name="home/profile.html"), name="profile"),
        path("login", auth_views.LoginView.as_view(), name="login"),
        path("logout", auth_views.LogoutView.as_view(), name="logout"),
        path("gtdadmin/", admin.site.urls),
        path("todo/", include("todo.urls", namespace="todo")),
    ]
    # Static media in DEBUG mode:
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
