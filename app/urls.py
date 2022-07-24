from app import views
from django.urls import path,include

urlpatterns = [
    path("",views.Home,name="Home"),
    path('contact',views.contact,name="contact"),
    path('signup',views.HandleSignup,name="HandleSignup"),
    path('login',views.HandleLogin,name="HandleLogin"),
    path('logout',views.HandleLogout,name="HandleLogout"),
    path("products",views.products,name="products"),
    path("orders",views.myorders,name="myorders"),
    path("orders/<id>",views.deleteOrder,name="deleteOrder"),
]
