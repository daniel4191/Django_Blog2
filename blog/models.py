import os

from django.db import models

# Create your models here.


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
    content = models.TextField()

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
    # author 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    # 이것을추가해 줌으로써 admin 페이지에서 볼때는 "View on site"라는 버튼이 생성되었다.
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    # 첨부파일의 이름을 확인
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 첨부파일의 확장자를 확인
    def get_file_ext(self):
        return self.file_name().split('.')[-1]
