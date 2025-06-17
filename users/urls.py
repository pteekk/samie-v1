from django.urls import path
from .views import UserViewSet, UserDetailView, LoginView, LogoutView

urlpatterns = [
    # GET /api/users/ - List all users
    # POST /api/users/ - Create new user
    path('', UserViewSet.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # GET /api/users/1/ - Retrieve user with id=1
    # PUT /api/users/1/ - Update user with id=1
    # PATCH /api/users/1/ - Partial update user with id=1
    # DELETE /api/users/1/ - Delete user with id=1
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]


