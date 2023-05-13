from django.urls import path, include
from . import views

urlpatterns = [
    # REGISTRATION URLS
    # path('accounts/login/', views.login_view), # django link set: LOGIN_URL = '/login/'
    # path('', include("django.contrib.auth.urls")), # all functionality is implemented in custom links above
    path('sign_up/', views.sign_up, name="sign_up"),
    path('activation_sent/', views.activation_sent, name="activation_sent"),
    path('reactivate/<str:email>/', views.reactivate_user, name='reactivate_user'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation/success/', views.activation_success, name='activation_success'),
    path('activation/error/', views.activation_error, name='activation_error'),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('password_change/', views.PasswordChange.as_view(template_name='registration/pass_change.html'), name="password_change"),
    path('password_change/done/', views.passwordChange_Done, name="password_change_done"),
    path('password_reset/', views.PasswordReset.as_view(template_name='registration/pass_reset.html'), name="password_reset"),
    path('password_reset/sent/', views.passwordReset_Sent, name="password_reset_sent"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(template_name='registration/pass_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset/done/', views.passwordReset_Done, name="password_reset_done"),
    path('profile/', views.profile, name='user_profile'),
    path('profile/<uuid:pk>', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/delete/', views.profile_delete, name='delete_user'),
]
