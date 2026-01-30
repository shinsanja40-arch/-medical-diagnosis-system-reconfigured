# Real-time Referee-Mediated Medical Diagnosis System
# 실시간 심판 개입 및 순환 중첩 구조 기반 고정밀 의료 진단 시스템

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

This system implements an advanced medical diagnosis framework using:
- **Circular Overlap Structure**: Multiple specialist groups with overlapping expertise
- **Referee-Mediated Debate**: Asymmetric debate protocol with strict hallucination control
- **Multi-agent Collaboration**: Neutral medical specialists working in coordinated groups

### Key Features

- ✅ Structured medical inquiry (one question at a time)
- ✅ Dynamic specialist selection based on symptoms
- ✅ Circular overlap group formation (e.g., Group1: A+B, Group2: B+C)
- ✅ 5-stage debate protocol with referee intervention
- ✅ Automatic hallucination detection and correction
- ✅ Stagnation detection (10-round repetition check)
- ✅ Maximum 100 rounds with parallel output on disagreement
- ✅ Persona reset mechanism for non-compliant agents
- ✅ **Web search integration** for latest medical information
- ✅ **Medical image analysis** (X-rays, skin conditions, CT scans, etc.)
- ✅ **Multi-language support** (Korean/English)

## 🏗️ System Architecture

```
User Input
    ↓
Diagnostic Medicine Specialist (문진)
    ↓
Specialist Selection & Group Formation
    ↓
Circular Overlap Debate Groups
    ↓
5-Stage Debate Protocol
    ├── Opinion
    ├── Referee Check
    ├── Cross-Counter
    ├── Rebuttal
    └── Final Judgment
    ↓
Diagnosis Output
```

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/medical-diagnosis-system.git
cd medical-diagnosis-system

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Anthropic API key
```

## 📦 Requirements

- Python 3.8+
- anthropic>=0.25.0
- python-dotenv>=1.0.0

## 💻 Usage

### Basic Usage

```python
from medical_diagnosis_system import MedicalDiagnosisSystem

# Initialize the system
system = MedicalDiagnosisSystem(api_key="your-api-key")

# Start diagnosis (interactive mode)
system.start_diagnosis()
```

### With Medical Images

```python
system = MedicalDiagnosisSystem(api_key="your-api-key")

# Add images before starting
system.add_medical_image("xray.jpg", "Chest X-ray")
system.add_medical_image("skin_photo.png", "Skin rash on arm")

# Start diagnosis
system.start_diagnosis()
```

### With Web Search (Latest Medical Information)

```python
system = MedicalDiagnosisSystem(api_key="your-api-key")

# Enable web search (enabled by default)
system.enable_web_search = True

# System will automatically search for:
# - Latest treatment guidelines
# - Recent research on rare conditions
# - Current diagnostic criteria

system.start_diagnosis()
```

### Multi-language Support

```python
system = MedicalDiagnosisSystem(api_key="your-api-key")

# Set language (Korean or English)
system.language = "en"  # or "ko"

system.start_diagnosis()
```

### Command Line Interface

```bash
python main.py
```

### Example Interaction

```
실시간 심판 개입 및 순환 중첩 구조 기반 고정밀 의료 진단 시스템
Real-time Referee-Mediated Medical Diagnosis System

💡 기능:
  - 의료 이미지 분석 (X-ray, 피부 사진 등)
  - 웹 검색을 통한 최신 의학 정보 조회
  - 다국어 지원 (한국어/English)

언어를 선택하세요 (1: 한국어, 2: English) [1]: 1

의료 이미지가 있으신가요? (y/n) [n]: y

📷 의료 이미지 업로드
지원 형식: JPG, PNG, GIF, WebP
예시: X-ray, 피부 병변, CT 스캔 등

이미지 파일 경로 (완료하려면 Enter): /path/to/xray.jpg
이미지 설명 (선택사항): 흉부 X-ray
✓ 이미지 추가됨: xray.jpg

이미지 파일 경로 (완료하려면 Enter): 

✓ 총 1개 이미지 추가됨

[진단의학과] 안녕하세요. 진단을 시작하겠습니다.
[진단의학과] 먼저 나이와 성별을 알려주시겠습니까?

> 35세 남성입니다

[진단의학과] 현재 복용 중인 약이나 진단받은 만성 질환이 있으십니까?

> 없습니다

[진단의학과] 어떤 증상으로 방문하셨습니까?

> 가슴 통증과 호흡곤란이 있습니다

🔍 웹 검색: 흉통 호흡곤란 원인

...
```

## 📚 System Components

### 1. Diagnostic Medicine Specialist (문진 담당)
- Conducts structured medical inquiry
- Asks one question at a time
- Mandatory checks: age, gender, chronic conditions, medications, family history
- **Analyzes uploaded medical images** (X-rays, skin photos, etc.)
- **Uses web search** for latest medical information

### 2. Referee Agent (심판)
- Monitors all debates for hallucinations
- Enforces debate protocol
- Intervenes on stagnation (10-round repetition)
- Resets non-compliant agents
- **Verifies medical evidence using web search**

### 3. Specialist Agents (전문의)
- Neutral expert stance (no bias)
- Circular overlap group participation
- 5-stage debate participation
- **Analyzes medical images when provided**
- **References latest research via web search**

### 4. Medical Image Analysis
Supports analysis of:
- X-rays (chest, abdomen, bone)
- CT and MRI scans
- Skin condition photos
- Endoscopy images
- Pathology slides
- Wound/injury photos

**Supported formats:** JPEG, PNG, GIF, WebP

### 5. Web Search Integration
Automatically searches for:
- Latest treatment guidelines (e.g., "COVID-19 treatment 2026")
- Rare disease diagnostic criteria
- Recent medical research
- Current drug information
- Differential diagnosis support

**Search is triggered when:**
- Specialists need latest information
- Referee validates medical claims
- Rare or complex conditions are suspected

### 4. Debate Protocol

**Stage 1: Opinion**
- Each specialist presents initial diagnosis

**Stage 2: Referee Check**
- Validates opinions against medical evidence
- Flags hallucinations or unsupported claims

**Stage 3: Cross-Counter**
- Specialists challenge each other's opinions

**Stage 4: Rebuttal**
- Defense against challenges

**Stage 5: Final Judgment**
- Referee determines consensus or valid disagreements

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
max_debate_rounds: 100
stagnation_threshold: 10
min_specialists: 2
max_specialists: 6
debate_detail_output: false  # Hide internal debate by default
```

## 🔬 Research & Citation

If you use this system in your research, please cite:

```bibtex
@software{medical_diagnosis_system,
  title={Real-time Referee-Mediated Medical Diagnosis System},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/medical-diagnosis-system}
}
```

## ⚠️ Disclaimer

This system is designed for research purposes and should not replace professional medical diagnosis. Always consult qualified healthcare providers for medical decisions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📧 Contact

For questions or collaboration inquiries, please open an issue on GitHub.

## 🙏 Acknowledgments

- Based on multi-agent debate frameworks
- Inspired by clinical diagnostic protocols
- Built with Anthropic's Claude API
