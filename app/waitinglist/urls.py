from django.urls import path, include
from django.views.generic import TemplateView

from . import views

#app_name = "pinax_waitinglist"

urlpatterns = [
    path('list_signup/', TemplateView.as_view(
        template_name="pinax/waitinglist/list_signup.html"), name="list_signup/"),
    path('', views.ListSignupView.as_view(), name="home"),
    path('ajax_list_signup/', views.ajax_list_signup, name="ajax_list_signup"),
    path('survey/thanks/', TemplateView.as_view(template_name="pinax/waitinglist/thanks.html"),
         name="survey_thanks"),
    path('survey/<code>/', views.SurveyView.as_view(), name="survey"),
    path('success/', TemplateView.as_view(template_name='pinax/waitinglist/success.html'),
         name="success"),
]
