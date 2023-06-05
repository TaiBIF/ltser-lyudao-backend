from django.urls import path
from .views import ContactAPIView, LiteratureAPIView, RegisterAPIView


urlpatterns = [
    path('auth/signUp/', RegisterAPIView.as_view(), name='signUp'),
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/literatures/', LiteratureAPIView.as_view(), name='literature'),
]