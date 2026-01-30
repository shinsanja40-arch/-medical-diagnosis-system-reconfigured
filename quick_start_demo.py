#!/usr/bin/env python3
"""
Quick Start Demo - 빠른 시작 데모
Demonstrates all key features of the Medical Diagnosis System
"""

import os
from medical_diagnosis_system import MedicalDiagnosisSystem, PatientInfo


def demo_basic():
    """기본 대화형 진단 데모"""
    print("=" * 70)
    print("DEMO 1: 기본 대화형 진단")
    print("=" * 70)
    print()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경 변수를 설정하세요.")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    system = MedicalDiagnosisSystem(api_key=api_key)
    
    print("✅ 시스템 초기화 완료")
    print("✅ 웹 검색: 활성화")
    print("✅ 이미지 분석: 활성화")
    print()
    
    # 대화형 시작
    system.start_diagnosis()


def demo_with_images():
    """이미지 포함 진단 데모"""
    print("=" * 70)
    print("DEMO 2: 의료 이미지 분석")
    print("=" * 70)
    print()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경 변수를 설정하세요.")
        return
    
    system = MedicalDiagnosisSystem(api_key=api_key)
    
    print("의료 이미지 예제:")
    print("  - X-ray, CT, MRI")
    print("  - 피부 병변 사진")
    print("  - 상처/부상 사진")
    print()
    
    # 이미지 경로 입력
    image_path = input("이미지 파일 경로를 입력하세요 (예: /path/to/xray.jpg): ").strip()
    
    if image_path and os.path.exists(image_path):
        description = input("이미지 설명 (예: 흉부 X-ray): ").strip()
        
        if system.add_medical_image(image_path, description):
            print()
            print("✅ 이미지가 성공적으로 추가되었습니다!")
            print("   전문의들이 이미지를 분석하여 진단에 참고합니다.")
            print()
            
            # 환자 정보 수동 입력 (데모용)
            system.patient_info.age = int(input("나이: "))
            system.patient_info.gender = input("성별 (남성/여성): ")
            system.patient_info.symptoms = input("증상 (쉼표로 구분): ").split(',')
            system.patient_info.symptoms = [s.strip() for s in system.patient_info.symptoms]
            
            system.inquiry_complete = True
            
            print()
            print("진단을 시작합니다...")
            print()
            
            system._start_diagnosis_debate()
    else:
        print("❌ 이미지 파일을 찾을 수 없습니다.")


def demo_multilingual():
    """다국어 지원 데모"""
    print("=" * 70)
    print("DEMO 3: Multi-language Support (English Mode)")
    print("=" * 70)
    print()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Please set ANTHROPIC_API_KEY environment variable.")
        return
    
    system = MedicalDiagnosisSystem(api_key=api_key)
    
    # 영어 모드 설정
    system.language = "en"
    
    print("✅ System initialized")
    print("✅ Language: English")
    print("✅ Web search: Enabled")
    print()
    
    # 영어로 진단 시작
    system.start_diagnosis()


def demo_programmatic():
    """프로그래밍 방식 진단 데모"""
    print("=" * 70)
    print("DEMO 4: 프로그래밍 방식 사용 (Programmatic Usage)")
    print("=" * 70)
    print()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경 변수를 설정하세요.")
        return
    
    system = MedicalDiagnosisSystem(api_key=api_key)
    
    print("예제: 두통 환자 진단")
    print()
    
    # 환자 정보 직접 설정
    system.patient_info = PatientInfo(
        age=35,
        gender="남성",
        symptoms=["두통", "어지러움", "메스꺼움"],
        chronic_conditions=[],
        medications=[]
    )
    
    system.inquiry_complete = True
    
    print("환자 정보:")
    print(f"  나이: {system.patient_info.age}")
    print(f"  성별: {system.patient_info.gender}")
    print(f"  증상: {', '.join(system.patient_info.symptoms)}")
    print()
    
    print("진단 시작...")
    print("(전문의들이 웹 검색을 통해 최신 정보를 조회합니다)")
    print()
    
    system._start_diagnosis_debate()


def demo_web_search():
    """웹 검색 기능 데모"""
    print("=" * 70)
    print("DEMO 5: 웹 검색 기능 (Web Search for Latest Info)")
    print("=" * 70)
    print()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경 변수를 설정하세요.")
        return
    
    system = MedicalDiagnosisSystem(api_key=api_key)
    
    print("웹 검색 기능:")
    print("  ✓ 최신 진료 가이드라인")
    print("  ✓ 희귀 질환 정보")
    print("  ✓ 최신 의학 연구")
    print("  ✓ 약물 상호작용")
    print()
    
    # 복잡한 증상 (웹 검색 필요)
    system.patient_info = PatientInfo(
        age=45,
        gender="여성",
        symptoms=[
            "근육 약화",
            "피로",
            "안검하수",
            "복시"
        ],
        chronic_conditions=[]
    )
    
    system.inquiry_complete = True
    
    print("복잡한 증상으로 진단 시작...")
    print("전문의들이 웹 검색으로 희귀 질환 정보를 조회합니다.")
    print()
    print("🔍 웹 검색이 자동으로 수행됩니다...")
    print()
    
    system._start_diagnosis_debate()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("의료 진단 시스템 - 빠른 시작 데모")
    print("Medical Diagnosis System - Quick Start Demo")
    print("=" * 70)
    print()
    
    print("사용 가능한 데모:")
    print()
    print("  1. 기본 대화형 진단")
    print("  2. 의료 이미지 분석")
    print("  3. 영어 모드 (Multi-language)")
    print("  4. 프로그래밍 방식 사용")
    print("  5. 웹 검색 기능")
    print()
    
    choice = input("실행할 데모 번호 (1-5): ").strip()
    print()
    
    demos = {
        "1": demo_basic,
        "2": demo_with_images,
        "3": demo_multilingual,
        "4": demo_programmatic,
        "5": demo_web_search
    }
    
    demo_func = demos.get(choice)
    if demo_func:
        demo_func()
    else:
        print("❌ 잘못된 선택입니다.")
