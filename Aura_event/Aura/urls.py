from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('admin_add/', views.admin_add, name='admin_add'),
    path('admin_edit/<int:product_id>/', views.admin_edit, name='admin_edit'),
    path('admin_remove/<int:product_id>/', views.admin_remove, name='admin_remove'),
    path('event_page/<int:event_id>/', views.event_page, name='event_page'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # ---- razopay----- #
    path('index/<int:product_id>/', views.index, name='index'),
    path('order_ payment',views.order_payment,name='order_payment'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

      # ---- foodadd----- #
    path('food/', views.food_list, name='food_list'),
    path('food/add/', views.add_food, name='add_food'),
    path('food/edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('food/delete/<int:food_id>/', views.delete_food, name='delete_food'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)