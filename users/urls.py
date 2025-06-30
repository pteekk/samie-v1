from django.urls import path
from .views import SignupView, LoginView, ProfileUpdateView


from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login
    TokenRefreshView,     # Refresh
    TokenVerifyView       # Optional
)


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('logout/', LogoutView.as_view(), name='logout')
]


urlpatterns += [
    path('jwt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]





