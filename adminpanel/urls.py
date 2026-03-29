from django.urls import path
from .import views

urlpatterns=[
    path('admin/stats/',views.AdminStatsView.as_view(),name='admin-stats'),
    path('admin/products/',views.AdminProductListView.as_view(),name='admin-products'),
    path('admin/products/<int:pk>/',views.AdminProductDetailView.as_view(),name='admin-product-detail'),
    path('admin/users/',views.AdminUserListView.as_view(),name='admin-users'),
    path('admin/users/<int:pk>/toggle/',views.AdminUserBlockView.as_view(),name='admin-users-toggle'),
    path('admin/users/<int:pk>/block/',views.AdminUserBlockOnlyView.as_view(),name='admin-users-block'),
    path('admin/orders/',views.AdminOrderListview.as_view(),name='admin-orders'),
    path('admin/orders/<int:pk>/',views.AdminOrderDetailView.as_view(),name='admin-order-detail')


]