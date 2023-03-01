from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
   # ex : /polls/
   path('', views.IndexView.as_view(), name='index'),
   # ex : /polls/5/
   path('<int:pk>/', views.DetailView.as_view(), name='detalle'),
   # ex : /polls/5/result
   path('<int:pk>/result/', views.ResultView.as_view(), name='resultado'),
   # ex : /polls/5/vote
   path('<int:question_id>/vote/', views.vote, name='votos'),
   
]
