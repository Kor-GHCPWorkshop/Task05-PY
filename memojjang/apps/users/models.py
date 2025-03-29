from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """사용자 정의 모델
    
    Django의 기본 User 모델을 상속받아 추가 필드를 정의합니다.
    username, email, password는 AbstractUser에서 상속받습니다.
    """
    
    created_at = models.DateTimeField(
        verbose_name="가입일시",
        auto_now_add=True,
        help_text="사용자 계정이 생성된 일시입니다."
    )
    
    updated_at = models.DateTimeField(
        verbose_name="수정일시",
        auto_now=True,
        help_text="사용자 정보가 마지막으로 수정된 일시입니다."
    )

    class Meta:
        """사용자 모델의 메타데이터를 정의합니다."""
        db_table = "users"  # 테이블 이름
        verbose_name = "사용자"  # Admin 페이지에서 보여질 단수 이름
        verbose_name_plural = "사용자들"  # Admin 페이지에서 보여질 복수 이름
        ordering = ["-created_at"]  # 생성일시 기준 내림차순 정렬

    def __str__(self):
        """사용자의 문자열 표현을 반환합니다."""
        return f"{self.username}" 
