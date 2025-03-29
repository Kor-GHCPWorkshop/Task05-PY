from django.test import TestCase, Client
from django.urls import reverse
from .apps.users.models import User
from .apps.memos.models import Memo


class MemoAppIntegrationTest(TestCase):
    """메모 애플리케이션 통합 테스트"""
    
    def setUp(self):
        """테스트에 사용할 클라이언트 설정"""
        self.client = Client()
    
    def test_user_registration_and_memo_workflow(self):
        """사용자 등록부터 메모 관리까지의 전체 워크플로우 테스트"""
        
        # 1. 회원가입
        register_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complex-password123",
            "password2": "complex-password123"
        }
        response = self.client.post(reverse("register"), register_data)
        self.assertRedirects(response, reverse("memo_list"))
        
        # 회원가입이 성공했는지 확인
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "newuser@example.com")
        
        # 2. 메모 생성
        memo_data = {
            "title": "첫 번째 메모",
            "content": "이것은 통합 테스트에서 작성한 메모입니다."
        }
        response = self.client.post(reverse("memo_create"), memo_data)
        self.assertRedirects(response, reverse("memo_list"))
        
        # 메모가 성공적으로 생성되었는지 확인
        memo = Memo.objects.get(title="첫 번째 메모")
        self.assertEqual(memo.user, user)
        self.assertEqual(memo.content, "이것은 통합 테스트에서 작성한 메모입니다.")
        
        # 3. 메모 수정
        memo_edit_data = {
            "title": "수정된 메모",
            "content": "이 내용은 수정되었습니다."
        }
        response = self.client.post(
            reverse("memo_edit", args=[memo.pk]), 
            memo_edit_data
        )
        self.assertRedirects(response, reverse("memo_detail", args=[memo.pk]))
        
        # 메모가 성공적으로 수정되었는지 확인
        memo.refresh_from_db()
        self.assertEqual(memo.title, "수정된 메모")
        self.assertEqual(memo.content, "이 내용은 수정되었습니다.")
        
        # 4. 메모 상세 보기
        response = self.client.get(reverse("memo_detail", args=[memo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "수정된 메모")
        self.assertContains(response, "이 내용은 수정되었습니다.")
        
        # 5. 메모 삭제
        response = self.client.post(reverse("memo_delete", args=[memo.pk]))
        self.assertRedirects(response, reverse("memo_list"))
        
        # 메모가 성공적으로 삭제되었는지 확인
        self.assertFalse(Memo.objects.filter(pk=memo.pk).exists())
        
        # 6. 로그아웃
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        
        # 로그아웃 후 메모 목록에 접근하면 로그인 페이지로 리다이렉트되는지 확인
        response = self.client.get(reverse("memo_list"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("login") in response.url)
