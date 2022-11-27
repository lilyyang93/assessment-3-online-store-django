from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('category/<str:category>/', views.print_category_products, name="individual_category"),
    path('search/product/<str:product_id>/', views.individual_product_details, name="individual_product"),
    path('shopping-cart/', views.shopping_cart, name="shopping_cart"),
    path('search/not-found/<str:q>/', views.not_in_stock, name="not_in_stock"),
]

