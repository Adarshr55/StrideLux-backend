from django.urls import path
from .import views

urlpatterns=[
    path('orders/',views.OrderListView.as_view(),name='orders'),
    path('orders/<int:pk>/',views.OrderDetailView.as_view(),name='order-details'),
    path('orders/<int:pk>/create-payment/',views.CreateRazorpayOrderView.as_view(),name='create-payment'),
    path('orders/<int:pk>/verify-payment/',views.VerifyPaymentView.as_view(),name='verify-payment')

]