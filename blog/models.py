from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
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
