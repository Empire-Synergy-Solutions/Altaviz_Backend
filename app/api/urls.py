from django.urls import include, path
from users.views.administrator import AdministratorView
from users.views.moderator import ModeratorView, ModeratorDetail
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView
#from django.paths import path, re_path
#from users import views
#from core.views.homepage import HomePageView
#from .views import UserCreate, LoginView, UserDetail, ProfileView, ProfileDetail
from core.views.accept_invitation import AcceptInvitationView
from core.views.login import LoginView
from core.views.logout import LogoutView
from core.views.profile import ProfileView, ProfileDetail
from core.views.reset_password import ResetPasswordView
from core.views.update_password import UpdatePasswordView
from core.views.user import UserView, UserDetail
from fuelcredit.views.invitation import InvitationView
from fuelcredit.views.transfer import TransferView
from fuelcredit.views.wallet import WalletDetail

schema_view = get_swagger_view(title='Easy App API')

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('swagger-docs', schema_view),
    path('docs/', include_docs_urls(title='Easy App API')),
    #path('users/', include('users.paths')),
    # swagger docs
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    # Administrators
    path('administrators', AdministratorView.as_view()),

    # Moderators
    path('moderators', ModeratorView.as_view()),
    path('moderators/<int:pk>', ModeratorDetail.as_view()),
    #
    #path('users', views.UserListView.as_view()),
    #path('<int:pk>', UserDetail.as_view()),
    #path('profiles', ProfileView.as_view()),
    #path('profiles/<int:pk>', ProfileDetail.as_view()),
    #path('', HomePageView.as_view(), name='home'),
    # path("signup/", UserCreate.as_view(), name="user_create"),
    #path("login/", LoginView.as_view(), name="login"),
    #path('create/', views.CreateUserView.as_view(), name='create'),
    #path('token/', views.CreateTokenView.as_view(), name='token'),
    #path('me/', views.ManageUserView.as_view(), name='me'),
    # Accept invitation
    path('accept_invitation/', AcceptInvitationView.as_view()),

    # Login / logout
    path('login', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    # Password management
    path('reset_password/', ResetPasswordView.as_view()),
    path('update_password/', UpdatePasswordView.as_view()),

    # Profiles
    path('profiles/', ProfileView.as_view()),
    #path('profiles/(?P<profile_id>[\d]+)', ProfileDetail.as_view()),
    path('profiles/<int:pk>', ProfileDetail.as_view()),

    # Users
    path('users', UserView.as_view()),
    #path('users/(?P<user_id>[\d]+)', UserDetail.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),

    # Invitations
    path('invitations', InvitationView.as_view()),

    # Transfers
    path('transfers', TransferView.as_view()),

    # Wallets
    #path('wallets/(?P<user_id>[\d]+)', WalletDetail.as_view()),
    path('wallets/<int:pk>', WalletDetail.as_view()),

]
