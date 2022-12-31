from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    # auto_now_add는 "최초 저장시"에만 저장이 되고
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now는 "수정 후 save를 할때마다"최신화 되어 적용된다.
    updated_at = models.DateTimeField(auto_now=True)
    # author 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}]{self.title}'