from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('enter_email/',views.enter_email,name='enter_email'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('change_password/',views.change_password,name='change_password'),
    path('profile/',views.profile,name='profile'),
    path('seller_index/',views.seller_index,name='seller_index'),
    path('add_book/',views.add_book,name='add_book'),
    path('view_books/',views.view_books,name='view_books'),
    path('book_detail/<int:pk>/',views.book_detail,name='book_detail'),
    path('edit_book/<int:pk>/',views.edit_book,name='edit_book'),
    path('delete_book/<int:pk>/',views.delete_book,name='delete_book'),
    path('book/<str:bname>/',views.book,name='book'),
    path('user_book_detail/<int:pk>/',views.user_book_detail,name='user_book_detail'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_from_wishlist<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('search/',views.search,name='search'),
    path('validate_username/',views.validate_username,name='validate_username'),
    path('validate_login/',views.validate_login,name='validate_login'),

]
    
