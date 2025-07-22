from django.urls import path
from .views import *



urlpatterns = [
    path('thread/', ThreadListCreateView.as_view()),
    path('thread/<int:pk>/', ThreadRUDView.as_view()),
    path('thread/<int:thread_pk>/comments/', CommentListCreateView.as_view()),
    path('comment/<int:comment_pk>/', CommentRetrieveUpdateDestroyView.as_view()),
    path('thread/<int:thread_pk>/subscription/', SubscriptionListCreateView.as_view()),
    path('subscription/<int:subscription_pk>/', SubscriptionDeleteView.as_view()),
    
]
