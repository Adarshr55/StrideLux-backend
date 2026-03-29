from django.urls import path
from .import views 

urlpatterns=[
    path('wishlist/',views.Wishlistview.as_view(),name='wishlist'),
    path('wishlist/add/',views.WishlistAddView.as_view(),name='wishlist-add'),
    path('wishlist/<int:product_id>/',views.WishlistRemoveView.as_view(),name='wishlist-remove')
]