# 주요 기능 / Key Features

## ✨ 새로운 기능 (New Features)

### 1. 의료 이미지 분석 (Medical Image Analysis)

**지원 이미지:**
- X-ray (흉부, 복부, 뼈)
- CT, MRI 스캔
- 피부 병변 사진
- 내시경 이미지
- 병리 슬라이드
- 상처/부상 사진

**지원 형식:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

**사용 방법:**
```python
system = MedicalDiagnosisSystem(api_key="your-key")

# 이미지 추가
system.add_medical_image("chest_xray.jpg", "흉부 X-ray PA view")
system.add_medical_image("skin_rash.png", "팔 안쪽 발진")

# 진단 시작 (이미지가 자동으로 분석됨)
system.start_diagnosis()
```

**어떻게 작동하나요?**
1. 업로드한 이미지는 base64로 인코딩됩니다
2. Claude API에 이미지와 함께 전송됩니다
3. 각 전문의 그룹이 이미지를 분석합니다
4. 영상 소견이 진단에 반영됩니다

---

### 2. 웹 검색 통합 (Web Search Integration)

**자동 검색 시나리오:**
- 최신 진료 가이드라인 확인
- 희귀 질환 진단 기준 조회
- 최신 의학 연구 참조
- 약물 정보 및 상호작용
- 드문 증상 감별 진단

**예시:**
```
🔍 웹 검색: COVID-19 치료 가이드라인 2026
🔍 웹 검색: 중증근무력증 진단 기준
🔍 웹 검색: 두통 최신 치료법
```

**사용 방법:**
```python
system = MedicalDiagnosisSystem(api_key="your-key")

# 웹 검색 활성화 (기본값: True)
system.enable_web_search = True

# 시스템이 필요시 자동으로 검색
system.start_diagnosis()
```

**언제 검색이 수행되나요?**
1. **문진 단계**: 증상에 대한 최신 정보 확인
2. **전문의 선별**: 진료 가이드라인 참조
3. **진단 토론**: 의학적 근거 검증
4. **심판 검증**: 환각 방지를 위한 팩트 체크
5. **제3의 관점**: 희귀 질환 가능성 탐색

---

### 3. 다국어 지원 (Multi-language Support)

**지원 언어:**
- 한국어 (Korean) - `ko`
- English - `en`

**사용 방법:**

**한국어:**
```python
system = MedicalDiagnosisSystem(api_key="your-key")
system.language = "ko"
system.start_diagnosis()
```

**영어:**
```python
system = MedicalDiagnosisSystem(api_key="your-key")
system.language = "en"
system.start_diagnosis()
```

**인터랙티브 모드:**
```
언어를 선택하세요 (1: 한국어, 2: English) [1]: 2

💡 Features:
  - Medical image analysis (X-ray, skin photos, etc.)
  - Web search for latest medical information
  - Multi-language support (Korean/English)
```

---

## 🔧 핵심 시스템 기능 (Core System Features)

### 순환 중첩 구조 (Circular Overlap Structure)
```
전문의: [A, B, C, D]
그룹 1: A + B
그룹 2: B + C
그룹 3: C + D
그룹 4: D + A
```

**장점:**
- 모든 전문의가 2개 그룹에 참여
- 교차 검증을 통한 신뢰도 향상
- 다양한 관점 확보

### 5단계 토론 프로토콜 (5-Stage Debate Protocol)

1. **Opinion (의견 제시)**
   - 각 그룹이 독립적으로 진단
   - 이미지 분석 결과 포함
   - 웹 검색으로 최신 정보 참조

2. **Referee Check (심판 검증)**
   - 의학적 근거 확인
   - 환각(hallucination) 탐지
   - 웹 검색으로 팩트 체크

3. **Cross-Counter (교차 반박)**
   - 다른 그룹 의견에 대한 반박
   - 대안적 진단 제시

4. **Rebuttal (재반박)**
   - 반박에 대한 방어
   - 추가 근거 제시

5. **Final Judgment (최종 판단)**
   - 심판의 종합 판단
   - 합의 여부 결정

### 심판 개입 시스템 (Referee Intervention)

**교착 상태 감지 (Stagnation Detection):**
- 10라운드 동안 동일한 의견 반복 시 개입
- 2개 이견: 병렬 출력 후 종료
- 3개 이상: 제3의 관점 투입

**환각 방지 (Hallucination Prevention):**
- 모든 주장에 대한 근거 요구
- 웹 검색으로 실시간 검증
- 근거 없는 주장 즉시 정정

---

## 📊 사용 통계 및 성능

### 평균 진단 시간
- 간단한 증상: 5-10분
- 중간 복잡도: 10-20분
- 복잡한 경우: 20-30분

### API 사용량
- 기본 진단: 10-30 API 호출
- 이미지 포함: 15-40 API 호출
- 웹 검색 포함: 20-50 API 호출

### 지원 전문과
내과, 신경과, 정형외과, 이비인후과, 안과, 피부과,
정신건강의학과, 심장내과, 호흡기내과, 소화기내과,
내분비내과, 신장내과, 혈액종양내과, 류마티스내과,
감염내과, 영상의학과, 병리과, 응급의학과 등

---

## 🔒 안전 기능 (Safety Features)

### 환각 탐지 (Hallucination Detection)
- 실시간 의학적 근거 검증
- 웹 검색을 통한 팩트 체크
- 심판의 지속적 모니터링

### 편향 완화 (Bias Mitigation)
- 중립적 전문가 페르소나 강제
- 순환 중첩 구조로 다각적 검토
- 심판의 공정한 중재

### 무한 루프 방지 (Loop Prevention)
- 최대 라운드 제한 (100)
- 교착 상태 자동 감지
- 강제 종료 및 결과 출력

---

## 💡 실제 사용 예시

### 예시 1: 피부 발진 진단
```python
system = MedicalDiagnosisSystem(api_key="key")

# 피부 사진 추가
system.add_medical_image("rash1.jpg", "팔 발진")
system.add_medical_image("rash2.jpg", "근접 촬영")

# 환자 정보
system.patient_info = PatientInfo(
    age=35,
    gender="여성",
    symptoms=["발진", "가려움"]
)

system.inquiry_complete = True
system._start_diagnosis_debate()

# 결과: 피부과, 알레르기내과 협진
# 이미지 분석 + 웹 검색으로 정확한 진단
```

### 예시 2: 흉부 X-ray 분석
```python
system = MedicalDiagnosisSystem(api_key="key")

# X-ray 추가
system.add_medical_image("chest_xray.jpg", "흉부 X-ray PA")

# 환자 정보
system.patient_info = PatientInfo(
    age=62,
    gender="남성",
    symptoms=["기침", "호흡곤란"],
    chronic_conditions=["고혈압"]
)

system.inquiry_complete = True
system._start_diagnosis_debate()

# 결과: 영상의학과 + 호흡기내과 협진
# X-ray 소견 + 최신 가이드라인 참조
```

### 예시 3: 희귀 질환 진단
```python
system = MedicalDiagnosisSystem(api_key="key")
system.enable_web_search = True  # 웹 검색 필수

system.patient_info = PatientInfo(
    age=35,
    gender="여성",
    symptoms=[
        "근육 약화",
        "안검하수",
        "복시",
        "연하곤란"
    ]
)

system.inquiry_complete = True
system._start_diagnosis_debate()

# 🔍 웹 검색: 중증근무력증 진단 기준
# 🔍 웹 검색: 안검하수 감별진단
# 결과: 희귀 질환 가능성 탐지
```

---

## 📈 향후 개선 계획

1. **다중 모달 통합**
   - 음성 입력 지원
   - 동영상 분석 (내시경 등)
   - 실시간 바이탈 연동

2. **AI 학습**
   - 피드백 기반 학습
   - 진단 정확도 향상
   - 개인화된 진료

3. **의료 데이터베이스 연동**
   - ICD-10 코드 자동 매핑
   - 의학 문헌 검색
   - 임상시험 정보

4. **협업 도구**
   - 실제 의료진과 협업
   - 2차 소견 요청
   - 원격 진료 지원

---

## ❓ FAQ

**Q: 이미지 크기 제한이 있나요?**
A: 5MB 이하를 권장합니다. 큰 이미지는 자동으로 압축될 수 있습니다.

**Q: 웹 검색은 어떻게 작동하나요?**
A: Claude API의 web_search 도구를 사용하여 실시간으로 검색합니다.

**Q: 어떤 언어를 더 지원할 계획인가요?**
A: 일본어, 중국어, 스페인어 등을 계획 중입니다.

**Q: 오프라인에서도 작동하나요?**
A: 아니요, 인터넷 연결과 API 접근이 필요합니다.

**Q: 실제 의료 진단에 사용할 수 있나요?**
A: 연구 목적으로만 사용하세요. 실제 진단은 의사와 상담하세요.
