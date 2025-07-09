from django.urls import path

from .views import (AdminThresholdUpdateView, PasswordResetConfirmView,
                    PasswordResetRequestView, ThresholdUpdateView, UserDetailView,
                    UserListView, UserLoginView, UserRegistrationView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('threshold/', ThresholdUpdateView.as_view(), name='user-threshold-update'),
    path('threshold/<uuid:user_id>/', ThresholdUpdateView.as_view(), name='user-threshold-update-admin'),
    path('threshold/default/', AdminThresholdUpdateView.as_view(), name='default-threshold-update'),
]