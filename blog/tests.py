from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User

from .models import Post, Category, Tag, Comment


# Create your tests here.


class TestView(TestCase):
    # def test_post_list(self):
    #     self.assertEqual(2, 2)

    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump',
                                                   password='somepassword')
        self.user_obama = User.objects.create_user(username='obama',
                                                   password='somepassword')

        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programming = Category.objects.create(
            name='trump', slug='programming')
        self.category_music = Category.objects.create(
            name='music', slug='music')

        # 태그 테스트 start
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')
        # 태그 테스트 end

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='Hello World. We are the world',
            category=self.category_programming,
            author=self.user_trump
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='Hello World. We are the world',
            category=self.category_music,
            author=self.user_obama
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트 입니다.',
            content='category가 없을 수도 있죠.',
            author=self.user_obama
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='첫 번째 댓글입니다.'
        )

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(
            f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(
            f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_category_page(self):
        response = self.client.get(
            self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_post_list(self):
        '''
        old codes
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드 된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 네비게이션 바가 있다.
        # navbar = soup.nav
        # 1.5 Blog, About Me라는 문구가 내비게이션 바에 있다.
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)

        # 2.1 메인 영역에 기시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 '아직 게시물이 없습니다' 라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2.5 첫 번째 포스트 작성자(author)가 포스트 영역(post-area)에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_000.content, post_area.text)

        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='Hello World. We are the World',
            author=self.user_trump
        )

        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4 '아직 게시물이 업습니다'라는 문구는 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)
        '''

        # new code after defined setUp
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.post_001.author.username.upper(),
                      post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(),
                      post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(),
                      post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # post_000 = Post.objects.create(
        #     title='첫번째 포스트 입니다.',
        #     content='Hello World. We are the world',
        #     author=self.user_trump
        # )

        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

        # comment area
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)

        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 로그인하지 않으면 status code가 200이면 안된다.
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff가 아닌 trump가 로그인을 한다.
        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff인 obama로로그인을 한다.
        self.client.login(username='obama', password='somepassword')

        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        # 태그 테스트 코드
        tag_str_input = main_area.find('input', id='id_tag_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post', {
                'title': 'Post Form 만들기',
                'content': "Post Form 페이지를 만듭시다.",
                'tags_str': 'new tag; 한글 태그, python'
            })

        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'obama')

        # 태그 테스트
        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # 작성자(obama)가 접근하는 경우
        self.client.login(
            username=self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post - Blog', main_area.text)

        # 태그를 텍스트로 사용할 수 있게 하는 기능
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url, {
                'title': '세 번째 포스트를 수정했습니다.',
                'content': '안녕 세계? 우리는 하나!',
                'category': self.category_music.pk,
                'tags_str': '파이썬 공부; 한글 태그, some tag'
            },
            follow=True
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)

    def test_comment_form(self):
        # 테스트를 이미 댓글이 1개가 있는 상태에서 시작한다.
        self.assertEqual(Comment.objects.count(), 1)
        # 이 댓글은 self.post_001에 달려있는 댓글이기 때문에 self.post_001의 댓글개수도 1개 입니다.
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # 비 로그인 상태
        # 로그인 상태인지를 확인하는 테스트
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assretIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        # 로그인 한 상태
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/', {
                'content': '오바마의 댓글입니다.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        new_comment = Comment.objects.last()

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find(
            'div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)

    def test_comment_update(self):
        # 댓글을 작성한 사람이 있어야 하므로, comment_by_trump생성
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )

        # 비 로그인 상태에서는 댓글이 2개 있는 self.post_001 페이지를 연다.
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 댓글 영역에 수정 버튼이 둘 다 보이지 않아야 하므로 수정 버튼의 id는 comment-해당 comment의 pk-update-btn
        # 으로 만든다.
        commet_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        # 로그인 한 상태 - obama가 로그인 했다는 가정
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # obama가 로그인을 했다는 가정이니, obama외의 댓글에 대해서는 edit이 보이지 않아야 한다.
        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find(
            'a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(
            comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        # edit 버튼을 누르면 댓글을 수정 하는 폼으로 이동
        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find(
            'textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        # 댓글에 대한 내용을 수정후, submit버튼을 클릭하면 실질적으로 수정됨
        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': '오바마의 댓글을 수정합니다.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

    # 삭제 기능
    def test_delete_comment(self):
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        # 비 로그인 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-delete-btn'))

        # trump로 로그인한 상태
        self.client.login(username='trump', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        comment_002_delete_modal_btn = comment_area.find(
            'a', id='comment-2-delete-modal-btn'
        )
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        self.assertEqual(
            comment_002_delete_modal_btn.attrs['data-target'],
            '#deleteCommentModal-2'
        )

        # 삭제할지 재차 묻는 modal
        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete', really_delete_btn_002.text)
        self.assertEqual(
            really_delete_btn_002.attrs['href'],
            'blog/delete_comment/2/'
        )

        response = self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(self.post_001.title, soup.title.text)
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('트럼프의 댓글입니다.', comment_area.text)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

    def test_search(self):
        post_about_python = Post.objects.create(
            title='파이썬에 대한 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump
        )

        response = self.client.get('/blog/search/파이썬/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')

        self.assertIn('Search: 파이썬 (2)', main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_about_python.title, main_area.text)
