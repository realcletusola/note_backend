from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView, 
    TokenObtainPairView
    )


from .views import (
    RegisterView,
    LogoutView,
    LogoutAllViews,
    UpdateEmailView,
    PasswordChangeView
    )


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllViews.as_view(), name='logout_all'),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    path('change_password/', PasswordChangeView.as_view(), name="change_password"),
]
