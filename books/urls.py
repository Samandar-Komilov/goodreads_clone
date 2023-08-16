from django.urls import path
from .views import landing_page
from . import views

app_name = "books"
urlpatterns = [
    path('', views.BookView.as_view(), name='list'),
    path('<int:id>/', views.BookDetailView.as_view(), name='detail')
]
