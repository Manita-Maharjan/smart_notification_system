from django.urls import path
from .views import *

urlpatterns = [
    path('user/', UserListCreateView.as_view()),
    path('me/', UserRetrieveView.as_view()),

    path('<int:pk>/',UserRUDView.as_view()),
    path('<int:pk>/login/', UserLoginListCreateView.as_view()),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),


   
]