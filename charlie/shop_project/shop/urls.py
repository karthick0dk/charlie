
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_add'),
    path('products/edit/<int:pk>/', views.product_update, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),


]
