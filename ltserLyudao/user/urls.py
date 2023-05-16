from django.urls import path
from .views import ContactAPIView, LiteratureAPIView, RegisterAPIView


urlpatterns = [
    path('auth/signUp/', RegisterAPIView.as_view(), name='signUp'),
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/contacts/<int:contact_id>/', ContactAPIView.as_view(), name='contact-detail'),
    path('users/literatures/', LiteratureAPIView.as_view(), name='literature'),
    path('users/literatures/<int:contact_id>/', LiteratureAPIView.as_view(), name='literature-detail'),
]