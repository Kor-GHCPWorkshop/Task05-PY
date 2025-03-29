from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserModelTest(TestCase):
    """사용자 모델 테스트"""
    
    def setUp(self):
        """테스트에 사용할 사용자 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )
    
    def test_user_creation(self):
        """사용자 생성 테스트"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword123"))
    
    def test_user_str_representation(self):
        """사용자 문자열 표현 테스트"""
        self.assertEqual(str(self.user), "testuser")


class UserViewTest(TestCase):
    """사용자 뷰 테스트"""
    
    def setUp(self):
        """테스트에 사용할 클라이언트와 사용자 설정"""
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        
        # 테스트 사용자 생성
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )
    
    def test_user_registration_view_get(self):
        """회원가입 페이지 접근 테스트"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
    
    def test_user_registration_view_post(self):
        """회원가입 처리 테스트"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        # 회원가입 성공 시 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, reverse("memo_list"))
        # 새 사용자가 데이터베이스에 생성되었는지 확인
        self.assertTrue(User.objects.filter(username="newuser").exists())
    
    def test_login_view_get(self):
        """로그인 페이지 접근 테스트"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
    
    def test_login_view_post_success(self):
        """로그인 성공 테스트"""
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, data)
        # 로그인 성공 시 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, reverse("memo_list"))
    
    def test_login_view_post_invalid_credentials(self):
        """잘못된 인증 정보로 로그인 시도 테스트"""
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        # 로그인 실패 시 로그인 페이지에 머무름
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
    
    def test_logout_view(self):
        """로그아웃 테스트"""
        # 먼저 로그인
        self.client.login(username="testuser", password="testpassword123")
        # 로그아웃
        response = self.client.get(self.logout_url)
        # 로그아웃 후 홈페이지로 리다이렉트
        self.assertRedirects(response, reverse("home"))
