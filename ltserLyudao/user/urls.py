from django.urls import path
from .views import ContactAPIView, LiteratureAPIView, RegisterAPIView, QATagAPIView, QuestionAnswerAPIView, FormLinkAPIVIew


urlpatterns = [
    path('auth/signUp/', RegisterAPIView.as_view(), name='signUp'),
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/literatures/', LiteratureAPIView.as_view(), name='literature'),
    path('users/qatags/', QATagAPIView.as_view(), name='qatag'),
    path('users/question-answers/', QuestionAnswerAPIView.as_view(), name='question-answers'),
    path('users/form-link/', FormLinkAPIVIew.as_view(), name='form-link'),
]
