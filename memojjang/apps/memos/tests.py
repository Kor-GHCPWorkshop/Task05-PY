from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Memo

User = get_user_model()


class MemoModelTest(TestCase):
    """메모 모델 테스트"""
    
    def setUp(self):
        """테스트에 사용할 사용자와 메모 생성"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )
        self.memo = Memo.objects.create(
            user=self.user,
            title="테스트 메모",
            content="테스트 내용입니다."
        )
    
    def test_memo_creation(self):
        """메모 생성 테스트"""
        self.assertEqual(self.memo.title, "테스트 메모")
        self.assertEqual(self.memo.content, "테스트 내용입니다.")
        self.assertEqual(self.memo.user, self.user)
    
    def test_memo_str_representation(self):
        """메모 문자열 표현 테스트"""
        self.assertEqual(str(self.memo), "테스트 메모")


class MemoViewTest(TestCase):
    """메모 뷰 테스트"""
    
    def setUp(self):
        """테스트에 사용할 클라이언트, 사용자, 메모 설정"""
        self.client = Client()
        # 테스트 사용자 생성 및 로그인
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )
        self.client.login(username="testuser", password="testpassword123")
        
        # 테스트용 메모 생성
        self.memo = Memo.objects.create(
            user=self.user,
            title="테스트 메모",
            content="테스트 내용입니다."
        )
        
        # URL 설정
        self.home_url = reverse("home")
        self.memo_list_url = reverse("memo_list")
        self.memo_create_url = reverse("memo_create")
        self.memo_detail_url = reverse("memo_detail", args=[self.memo.pk])
        self.memo_edit_url = reverse("memo_edit", args=[self.memo.pk])
        self.memo_delete_url = reverse("memo_delete", args=[self.memo.pk])
    
    def test_home_view(self):
        """홈 페이지 접근 테스트"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
    
    def test_memo_list_view(self):
        """메모 목록 페이지 접근 테스트"""
        response = self.client.get(self.memo_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_list.html")
        # 목록에 생성한 메모가 포함되어 있는지 확인
        self.assertContains(response, "테스트 메모")
    
    def test_memo_create_view_get(self):
        """메모 생성 페이지 접근 테스트"""
        response = self.client.get(self.memo_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
    
    def test_memo_create_view_post(self):
        """메모 생성 처리 테스트"""
        data = {
            "title": "새 메모",
            "content": "새 메모의 내용입니다."
        }
        response = self.client.post(self.memo_create_url, data)
        # 메모 생성 성공 시 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, self.memo_list_url)
        # 새 메모가 데이터베이스에 생성되었는지 확인
        self.assertTrue(Memo.objects.filter(title="새 메모").exists())
    
    def test_memo_detail_view(self):
        """메모 상세 페이지 접근 테스트"""
        response = self.client.get(self.memo_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_detail.html")
        # 상세 페이지에 메모 내용이 표시되는지 확인
        self.assertContains(response, "테스트 메모")
        self.assertContains(response, "테스트 내용입니다.")
    
    def test_memo_edit_view_get(self):
        """메모 수정 페이지 접근 테스트"""
        response = self.client.get(self.memo_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_form.html")
    
    def test_memo_edit_view_post(self):
        """메모 수정 처리 테스트"""
        data = {
            "title": "수정된 메모",
            "content": "수정된 내용입니다."
        }
        response = self.client.post(self.memo_edit_url, data)
        # 메모 수정 성공 시 메모 상세 페이지로 리다이렉트
        self.assertRedirects(response, reverse("memo_detail", args=[self.memo.pk]))
        # 메모가 데이터베이스에서 수정되었는지 확인
        self.memo.refresh_from_db()
        self.assertEqual(self.memo.title, "수정된 메모")
        self.assertEqual(self.memo.content, "수정된 내용입니다.")
    
    def test_memo_delete_view_get(self):
        """메모 삭제 확인 페이지 접근 테스트"""
        response = self.client.get(self.memo_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "memos/memo_confirm_delete.html")
    
    def test_memo_delete_view_post(self):
        """메모 삭제 처리 테스트"""
        response = self.client.post(self.memo_delete_url)
        # 메모 삭제 성공 시 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, self.memo_list_url)
        # 메모가 데이터베이스에서 삭제되었는지 확인
        self.assertFalse(Memo.objects.filter(pk=self.memo.pk).exists())
    
    def test_login_required(self):
        """로그인 필요한 뷰에 대한 테스트"""
        # 로그아웃
        self.client.logout()
        
        # 각 뷰에 접근 시도 및 리다이렉트 확인
        for url in [self.memo_list_url, self.memo_create_url, 
                   self.memo_detail_url, self.memo_edit_url, 
                   self.memo_delete_url]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # 리다이렉션 확인
            # 로그인 페이지로 리다이렉트되는지 확인
            self.assertTrue(reverse("login") in response.url)
