#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
상담 관리 시스템 실행 스크립트
Python Flask 기반 독립형 애플리케이션

사용법:
    python run.py

접속 주소:
    http://localhost:9000

테스트 계정:
    학생: student1 / password123
    교수: professor1 / password123
"""

import os
import sys

# 현재 디렉토리를 Python path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from app import app
    
    if __name__ == '__main__':
        print("=" * 60)
        print("🎓 상담 관리 시스템 - Python Flask 독립형 애플리케이션")
        print("=" * 60)
        print("🚀 서버 시작 중...")
        print("📱 접속 주소: http://localhost:9000")
        print("🌐 네트워크 접속: http://0.0.0.0:9000")
        print()
        print("👤 테스트 계정:")
        print("   🎒 학생1: student1 / password123")
        print("   🎒 학생2: student2 / password123")  
        print("   👨‍🏫 교수1: professor1 / password123")
        print("   👨‍🏫 교수2: professor2 / password123")
        print()
        print("⚡ 기능:")
        print("   • 학생: 상담 요청 작성, 진행상황 확인")
        print("   • 교수: 상담 요청 관리, 피드백 제공")
        print("   • 실시간 상태 업데이트")
        print("   • 반응형 웹 디자인")
        print()
        print("🛑 종료하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=9000)
        
except ImportError as e:
    print("❌ Flask 모듈을 찾을 수 없습니다.")
    print("📦 다음 명령어로 Flask를 설치하세요:")
    print("   pip install flask")
    print(f"오류 상세: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ 애플리케이션 시작 중 오류가 발생했습니다: {e}")
    sys.exit(1)