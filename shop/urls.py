from django.urls import path

from shop.views import ProductList, ProductListByCategory, ProductDetail, login_register, user_register, user_login, \
    user_logout, LikeView, user_like, cart, to_cart, payment, success_payment, save_comment

urlpatterns = [
    path('',ProductList.as_view(),name='index'),
    path("category/<slug:slug>/", ProductListByCategory.as_view(), name="category"),
    path("product/<slug:slug>/", ProductDetail.as_view(), name="product"),
    path("login_register/", login_register, name="login_register"),
    path("user_register/", user_register, name="user_register"),
    path("user_login/", user_login, name="user_login"),
    path("user_logout/", user_logout, name="user_logout"),
    path("likes/", LikeView.as_view(), name="likes"),
    path("user_like/<slug:product_slug>/", user_like, name="user_like"),
    path("cart/", cart, name="cart"),
    path("to_cart/<int:product_id>/<str:action>/", to_cart, name="to_cart"),
    path("payment/", payment, name="payment"),
    path("success/", success_payment, name="success"),
    path('add_comment/<int:product_id>/', save_comment, name="save_comment"),

]