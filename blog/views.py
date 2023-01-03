from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag

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

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        # 이 코드는 "카테고리가 지정되지 않은 post의 갯수를 세어라"라는 뜻이다.
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()
        return context

# def single_post_page(request, pk):
#     post = Post.objects.get(pk = pk)
#
#     return render(request, 'blog/post_detail.html', {'post':post})

# 위의 single_post_page를 CBV 방식으로 대체


class PostDetail(DetailView):
    model = Post

    # DetailView도 ListView와 마찬가지로 template_name을 따로 지정해주면 그 파일로,
    # 그렇지 않으면 "post_detail.html"이라는 이름의 파일로 데이터셋을 보내게 된다.
    # 보통 각 CBV 방식에 대해서 template_name을 따로 지정하지 않으면 "어떤 이름으로 자동배정 되는가"가
    # 궁금하다면, 일단 실핼 했을때 에러 메세지로 나오게 된다.
    # 정확히는 동일한 앱 내에서만 데이터를 보내주는 것 같다.
    # 데이터셋을 전달할때는 ListView와는 약간 다르게 "<클래스명>"이다. 하지만 클래스명은 파이썬 문법적으로
    # 첫 문자는 대문자로 사용하는 반면, 전달되는 데이터셋은 대문자가 없는, 이를테면 Post를 model에 지정해줬다면
    # post라는 데이터셋이 post_detail.html이라는 이름의 파일로 가게된다 (template_name에 별도로 설정할경우 그곳으로)

    # 에러 메세지
    # TemplateDoesNotExist at /blog/2/
    # blog/post_detail.html

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()

        return context


# FBV 방식
def category_page(request, slug):
    # category = Category.objects.get(slug=slug)

    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        # 여기의 인자로 들어가는 값들은 이미 CBV 방식으로써 post_list.html에 전달되고 있기 때문에
        # 어떤 인자를 보낼지에 대해서는 "딕셔너리"형태로 보내야 한다.
        'blog/post_list.html', {
            # 또한 이미 PostList의 CBV방식으로써 전달된 인자들에 대해서 언급이 되어야 한다.
            # Post 중에서 Category.objects.get(slug=slug)로 필터링한 카테고리만 가져와줘
            'post_list': post_list,
            # 전체 카테고리
            'categories': Category.objects.all(),
            # post_list로 filtering한 개수를 알려줘
            'no_category_post_count': Post.objects.filter(category=None).count(),
            # category의 이름을 알려줘
            'category': category
        }
    )


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
        'tag': tag,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count()
    })
