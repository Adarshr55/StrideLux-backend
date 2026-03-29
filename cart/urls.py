from django.urls import path
from .import views
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartItemView.as_view(), name='cart-add'),
    path('cart/item/<int:pk>/',views.CartItemUpdateView.as_view(), name='cart-item'),
]