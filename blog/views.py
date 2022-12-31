from django.shortcuts import render
from django.views.generic import ListView

from .models import Post

# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(request, 'blog/post_list.html', {'posts':posts})

# 위의 index를 CBV 방식인 이것으로 대체
class PostList(ListView):
    model = Post
    # CBV 방식에 있어서 사용되는 첫번째 방법
    # template_name을 직접 지정해준다.
    # 하지만 기존의 FBV방식의 경우에는 모든 인자를 지정해서 html로 전송해줬었는데
    # CBV는 방식이 다르다.
    # 기본적으로 <사용되었던모델명>_list
    # 이게 전체 데이터가 된다. ListView에 한에서는 말이다.
    # 여기서는 model = Post로써 models에 정의되어있는 Post를 사용했기때문에
    # post_list가 된다. 그리고 이걸 html에서 인자로 사용하면 된다.
    # 하지만 만약 이렇게 template_name을 명시하지 않으면 post_list.html이라는 이름의 파일을
    # 자동으로 template_name으로 인식하게 된다.
    # template_name = 'blog/post_list.html'

    # CBV 방식에 있어서 사용되는 두번째 방법
    # 앞선 첫번째 방법에서 말했다시피 template_name을 지정하지 않으면
    # <model에 지정된 models의 클래스>_list.html이 자동으로 template_name으로 인식됨
    # 여기서는 기존에 사용하던 blog/index.html을 blog/post_list.html로 변경함.

    # 정렬순서를 업로드된 pk값(id값)을 기준하여 역순으로 정렬
    ordering = '-pk'


def single_post_page(request, pk):
    post = Post.objects.get(pk = pk)

    return render(request, 'blog/single_post_page.html', {'post':post})