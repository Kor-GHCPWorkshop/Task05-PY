"""
테스트 실행을 위한 도우미 스크립트
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # 테스트 모듈을 설정
    os.environ['DJANGO_SETTINGS_MODULE'] = 'memojjang.settings'
    
    # Django 초기화
    django.setup()
    
    # 테스트 러너 설정
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # 인자로 전달된 모듈 또는 전체 테스트 실행
    test_module_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    # 테스트 실행 및 결과 출력
    print("테스트 실행을 시작합니다...")
    failures = test_runner.run_tests([test_module_path])
    
    # 종료 코드 설정 (실패 시 1, 성공 시 0)
    sys.exit(bool(failures))
# No replacement needed; simply remove the invalid lines.
