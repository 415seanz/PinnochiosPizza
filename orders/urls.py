from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("cart", views.cart_view, name="cart"),
    path("orders", views.orders_view, name="orders"),
    path("staff", views.staff_view, name="staff"),
    path("staff/<int:ordernum>", views.vieworder_view, name="vieworder"),
    path("<slug:category>", views.category_view, name="category")
]
