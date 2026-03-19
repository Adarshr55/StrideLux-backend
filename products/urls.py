from django.urls import path
from .import views

urlpatterns=[
    path('categories/',views.CategoryListView.as_view(),name='categories'),
    path('products/',views.ProductListView.as_view(),name='products'),
    path('products/<int:pk>/',views.ProductDetailsView.as_view(),name='product-details')
]