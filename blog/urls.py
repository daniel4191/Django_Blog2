from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.index),
    # 위의 방식은 FBV 방식, 아래꺼는 CBV방식
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.single_post_page)
]