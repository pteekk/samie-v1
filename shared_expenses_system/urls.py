from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/wallets/', include('wallets.urls')),
    path('api/transactions/', include('transactions.urls')),  # To be created
]
