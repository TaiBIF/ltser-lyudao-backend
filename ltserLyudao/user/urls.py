from django.urls import path
from .views import ContactAPIView, LiteratureAPIView, RegisterAPIView, QATagAPIView, QuestionAnswerAPIView, \
    FormLinkAPIVIew, FormLinkDownloadAPIview, NewsTagAPIView, NewsAPIView, NewsDownloadAPIViews


urlpatterns = [
    path('auth/signUp/', RegisterAPIView.as_view(), name='signUp'),
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/literatures/', LiteratureAPIView.as_view(), name='literature'),
    path('users/qatags/', QATagAPIView.as_view(), name='qatag'),
    path('users/question-answers/', QuestionAnswerAPIView.as_view(), name='question-answers'),
    path('users/form-link/', FormLinkAPIVIew.as_view(), name='form-link'),
    path('users/download/form-link/', FormLinkDownloadAPIview.as_view(), name='form-link-attachments-download'),
    path('users/newstags/', NewsTagAPIView.as_view(), name='newsTag'),
    path('users/news/', NewsAPIView.as_view(), name='news'),
    path('users/download/news/', NewsDownloadAPIViews.as_view(), name='news-images-attachments-download'),
]
