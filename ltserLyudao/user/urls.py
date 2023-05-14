from django.urls import path
from .views import ContactAPIView


urlpatterns = [
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/contacts/<int:contact_id>/', ContactAPIView.as_view(), name='contact-detail'),
]