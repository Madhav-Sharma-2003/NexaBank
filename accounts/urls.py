from django.urls import path
from . import views, api_views

urlpatterns = [
    # ── Web URLs ──────────────────────────
    path('', views.landing_view, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search-user/', views.search_user, name='search_user'),

    # ── API URLs ──────────────────────────
    path('api/register/', api_views.api_register, name='api_register'),
    path('api/login/', api_views.api_login, name='api_login'),
    path('api/account/', api_views.api_account, name='api_account'),
    path('api/transactions/', api_views.api_transactions, name='api_transactions'),
    path('api/deposit/', api_views.api_deposit, name='api_deposit'),
    path('api/withdrawl/', api_views.api_withdrawal, name='api_withdrawl'),
    path('api/transfer/', api_views.api_transfer, name='api_transfer'),
]