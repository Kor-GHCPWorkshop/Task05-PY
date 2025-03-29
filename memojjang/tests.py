from django.test import TestCase
from .forms import MemoForm, UserRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class MemoFormTest(TestCase):
    """메모 폼 테스트"""
    
    def test_memo_form_valid_data(self):
        """유효한 데이터로 메모 폼 테스트"""
        form_data = {
            "title": "테스트 메모",
            "content": "테스트 내용입니다."
        }
        form = MemoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_memo_form_empty_data(self):
        """빈 데이터로 메모 폼 테스트"""
        form_data = {
            "title": "",
            "content": ""
        }
        form = MemoForm(data=form_data)
        self.assertFalse(form.is_valid())
        # title과 content 필드에 대한 에러 메시지가 있는지 확인
        self.assertIn("title", form.errors)
        self.assertIn("content", form.errors)


class UserRegistrationFormTest(TestCase):
    """사용자 회원가입 폼 테스트"""
    
    def test_user_registration_form_valid_data(self):
        """유효한 데이터로 회원가입 폼 테스트"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_registration_form_password_mismatch(self):
        """비밀번호 불일치 테스트"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "differentpassword"
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # 비밀번호 불일치에 대한 에러 메시지가 있는지 확인
        self.assertIn("password2", form.errors)
    
    def test_user_registration_form_missing_data(self):
        """누락된 데이터로 회원가입 폼 테스트"""
        # 필수 필드 중 하나를 누락
        form_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123"
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # username 필드에 대한 에러 메시지가 있는지 확인
        self.assertIn("username", form.errors)
