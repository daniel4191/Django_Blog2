import os

from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


class MyModel(models.Model):
    myfield = MarkdownxField()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    # unique = True를 하면 "동일한 name"을 가지는 카테고리를 중복해서 만들 수 없다.
    name = models.CharField(max_length=50, unique=True)

    # slug는 검색엔진의 정확도를 높이는데 도움을 준다.
    # blog/1/이런식으로 표기되던 것을 해당 포스트의 특징에 맞게 blog/text/이런식으로 된다고 한다.
    # 게다가 띄어쓰기가 있으면 blog/text-area/이런식으로 -를 자동으로 기입하여 이어붙인다고 한다.
    # slug는 기본적으로 한글을 지원하지 않기때문에, 한글을 사용하기 위해
    # allow_unicode = True를 해준것이다.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # 이건 사용자가 url주소만 봐도 무슨내용인지 알수있게끔 slug처리해주는 것

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # 이건 admin 페이지에서 "어떤 이름으로 노출될 것인가"를 정해주는 기능이다.

    class Meta:
        # verbose는 "말이 많다"를 의미
        # plural은 "복수"를 의미함 (단수,복수의 그 복수)
        verbose_name_plural = 'Categories'


# 사용법 설명
# def (함수)
# 기본적으로 class 내부에 정의되는 def 함수들은 추후, urls, views를 통해서 연결된 html에서
# <class명>.<함수명>으로 사용 가능하다
# 예시: {{ post.get_absolute_url }}

# title, hook_text, content같이 그냥 변수
# 클래스에 직접적으로 생성되어있는 변수들은
# 보통 urls, views를 통해서 연결된 html 파일에 데이터를 보내주며
# 기본적으로는 "반복문"조합으로 써준다.
# 이를테면 Post라는 하나의 클래스가 담고 있는 데이터셋은 views를 거쳐서 CBV방식의 경우
# post_list 라는 이름으로 보내지게 된다.
# 이런 "덩어리 데이터셋"을 for i in post_list
# 이런식으로 풀어주게 되고
# i.title, i.hook_"text, i.content
# 이런식으로 사용하게 되는 것이다.
class Post(models.Model):
    title = models.CharField(max_length=30)
    # 노출되는 글씨의 수를 제한적으로 보여주는 소제목의 용도로 사용하기 위해 만든다고 보면 될것같다
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    # 설명1. upload_to
    # 이거는 지정된 위치의 폴더에 연도/시간/일 단위로 쪼개서
    # 폴더를 분산해서 데이터베이스에 저장한다는 의미다.
    # 폴더를 분산하면 데이터를 서치하는게 용이하지만,
    # 하나의 폴더에서 여러개의 파일을 찾는것은 시간적으로 좋지 않다고 한다.

    # 설명2. blank = True
    # 필수로 채우지 않아도 상관없다는 의미
    # 즉, 이 경우에는 "이미지 업로드를 해도되고 안해도되"라는 의미
    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)

    # auto_now_add는 "최초 저장시"에만 저장이 되고
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now는 "수정 후 save를 할때마다"최신화 되어 적용된다.
    updated_at = models.DateTimeField(auto_now=True)

    # 기존 author 모델이고, 이대로 사용할 시, 작성자(author를 삭제하면 이 작성자가 작성한
    # 게시글은 모조리 삭제된다.
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    # SET_NULL을 하게되면 작성자 계정이 사라져도 게시글은 남아있다.
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 텍스트, 숫자의 null은 null이고, 계정, 카테고리등 목록선택창에서의 null은 blank이다.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    # 이것을추가해 줌으로써 admin 페이지에서 볼때는 "View on site"라는 버튼이 생성되었다.
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    # 첨부파일의 이름을 확인
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 첨부파일의 확장자를 확인
    def get_file_ext(self):
        return self.file_name().split('.')[-1]

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    # 이게 있음으로 인해서 실질적으로 작성된 댓글 확인이 가능하다.
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
