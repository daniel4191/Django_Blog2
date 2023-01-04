"""do_it_django_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', include('single_pages.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls'))
]

# 미디어 파일저장을 위한 것이라고는 하는데, 정확히 잘 모르겠다.
# 왜냐면 이미 파일저장을 위한 세팅들을 settings라든지 models에 등록해놓았기 때문이다.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
