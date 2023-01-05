from django.urls import path

from . import views

# 이건 각 app 단위의 urls 마다 자동적으로 써주면 좋은 것.
# 중복된 인자명을 배제하기 위해서이다.
# 예를들자면 blog라는 app과 love라는 app에서
# post_list라는 인자를 함께 사용할 경우, 사용에 내가 원하는 결과를 얻을 수 없다.
# app_name을 설정해줌으로 blog:post_list, love:post_list
# 이렇게 <앱이름>:<인자이름> 으로 써주는 것으로 알고있다.
app_name = 'blog'

urlpatterns = [
    # path('', views.index),
    # 위의 방식은 FBV 방식, 아래꺼는 CBV방식
    path('', views.PostList.as_view()),
    # path('<int:pk>/', views.single_post_page)
    # 위의 방식은 FBV 방식, 아래꺼는 CBV방식
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
]
