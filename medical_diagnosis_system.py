"""
Real-time Referee-Mediated Medical Diagnosis System
실시간 심판 개입 및 순환 중첩 구조 기반 고정밀 의료 진단 시스템

This module implements the core diagnostic system with:
- Circular overlap structure for specialist groups
- Referee-mediated debate protocol
- Hallucination detection and intervention
- Web search for medical information
- Image analysis for medical images (X-rays, skin conditions, etc.)
"""

import os
import json
import base64
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import anthropic
from datetime import datetime
from pathlib import Path


class DebateStage(Enum):
    """5-stage debate protocol"""
    OPINION = "opinion"
    REFEREE_CHECK = "referee_check"
    CROSS_COUNTER = "cross_counter"
    REBUTTAL = "rebuttal"
    FINAL_JUDGMENT = "final_judgment"


@dataclass
class PatientInfo:
    """Patient information collected during inquiry"""
    age: Optional[int] = None
    gender: Optional[str] = None
    chronic_conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    family_history: List[str] = field(default_factory=list)
    symptoms: List[str] = field(default_factory=list)
    additional_info: Dict = field(default_factory=dict)
    images: List[Dict[str, Any]] = field(default_factory=list)  # Medical images
    web_search_results: List[Dict] = field(default_factory=list)  # Search results


@dataclass
class DebateRound:
    """Single round of debate"""
    round_number: int
    stage: DebateStage
    speaker: str
    content: str
    referee_feedback: Optional[str] = None
    hallucination_detected: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class DiagnosisOpinion:
    """Diagnostic opinion from a specialist or group"""
    specialist: str
    diagnosis: str
    confidence: float
    reasoning: str
    evidence: List[str] = field(default_factory=list)


class MedicalDiagnosisSystem:
    """
    Main system class implementing the referee-mediated diagnosis protocol
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the medical diagnosis system
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        
        # System state
        self.patient_info = PatientInfo()
        self.inquiry_complete = False
        self.selected_specialists: List[str] = []
        self.specialist_groups: List[Tuple[str, str]] = []
        self.debate_history: List[DebateRound] = []
        self.current_round = 0
        self.max_rounds = 100
        self.stagnation_threshold = 10
        self.conversation_history: List[Dict] = []
        
        # Debate state tracking
        self.last_opinions: List[str] = []
        self.stagnation_count = 0
        self.active_opinions: List[DiagnosisOpinion] = []
        
        # Feature flags
        self.enable_web_search = True
        self.enable_image_analysis = True
        self.language = "ko"  # Default to Korean
        
    def _call_claude(self, system_prompt: str, user_message: str, use_tools: bool = False, images: Optional[List] = None) -> Tuple[str, List[Dict]]:
        """
        Make a call to Claude API with optional web search and image support
        
        Args:
            system_prompt: System instruction for Claude
            user_message: User's message
            use_tools: Whether to enable web search tool
            images: Optional list of images from patient_info
            
        Returns:
            Tuple of (response text, tool use information)
        """
        try:
            # Build message content
            message_content = []
            
            # Add images if provided (from patient_info.images)
            if images and len(images) > 0:
                for img_data in images:
                    message_content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": img_data.get("media_type", "image/jpeg"),
                            "data": img_data["data"]
                        }
                    })
                    if img_data.get("description"):
                        message_content.append({
                            "type": "text",
                            "text": f"[이미지: {img_data['description']}]"
                        })
            
            # Add text message
            message_content.append({
                "type": "text",
                "text": user_message
            })
            
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": 4000,
                "system": system_prompt,
                "messages": [{"role": "user", "content": message_content}]
            }
            
            # Add web search tool if requested
            if use_tools and self.enable_web_search:
                api_params["tools"] = [{
                    "type": "web_search_20250305",
                    "name": "web_search"
                }]
            
            # Make initial API call
            message = self.client.messages.create(**api_params)
            
            # Handle tool use (web search)
            if message.stop_reason == "tool_use":
                # Extract tool uses and text
                tool_uses = []
                assistant_text = ""
                
                for block in message.content:
                    if block.type == "text":
                        assistant_text += block.text
                    elif block.type == "tool_use":
                        tool_uses.append(block)
                
                # Continue conversation with tool results
                # Note: In real implementation, we'd process the actual search results
                # For now, we acknowledge that search was performed
                conversation_messages = [
                    {"role": "user", "content": message_content},
                    {"role": "assistant", "content": message.content}
                ]
                
                # Get final response after tool use
                final_message = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    system=system_prompt,
                    messages=conversation_messages
                )
                
                response_text = ""
                for block in final_message.content:
                    if block.type == "text":
                        response_text += block.text
                
                return response_text, [{"name": t.name, "input": t.input} for t in tool_uses]
            
            # No tool use - just return text
            response_text = ""
            for block in message.content:
                if block.type == "text":
                    response_text += block.text
            
            return response_text, []
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            raise
    
    def add_medical_image(self, image_path: str, description: str = "") -> bool:
        """
        Add a medical image to patient information
        
        Args:
            image_path: Path to the image file
            description: Optional description of the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(image_path)
            if not path.exists():
                print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
                return False
            
            # Read and encode image
            with open(path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine media type
            ext = path.suffix.lower()
            media_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            media_type = media_type_map.get(ext, 'image/jpeg')
            
            # Add to patient info
            self.patient_info.images.append({
                'data': image_data,
                'media_type': media_type,
                'filename': path.name,
                'description': description
            })
            
            print(f"✓ 이미지 추가됨: {path.name}")
            return True
            
        except Exception as e:
            print(f"이미지 추가 중 오류: {e}")
            return False
    
    def _web_search(self, query: str) -> List[Dict]:
        """
        Perform web search for medical information
        
        Args:
            query: Search query
            
        Returns:
            List of search results
        """
        if not self.enable_web_search:
            return []
        
        # Note: In the actual implementation with Claude API web search tool,
        # this would use the real web_search tool. For now, we'll prepare the structure.
        print(f"🔍 웹 검색: {query}")
        return []
    
    def start_diagnosis(self):
        """Start the diagnosis process with initial inquiry"""
        print("=" * 80)
        print("실시간 심판 개입 및 순환 중첩 구조 기반 고정밀 의료 진단 시스템")
        print("Real-time Referee-Mediated Medical Diagnosis System")
        print("=" * 80)
        print()
        print("💡 기능:")
        print("  - 의료 이미지 분석 (X-ray, 피부 사진 등)")
        print("  - 웹 검색을 통한 최신 의학 정보 조회")
        print("  - 다국어 지원 (한국어/English)")
        print()
        
        # Ask for language preference
        lang_input = input("언어를 선택하세요 (1: 한국어, 2: English) [1]: ").strip()
        if lang_input == "2":
            self.language = "en"
        
        # Ask about image upload
        img_input = input("\n의료 이미지가 있으신가요? (y/n) [n]: ").strip().lower()
        if img_input == 'y':
            self._upload_images()
        
        self._conduct_inquiry()
        
    def _upload_images(self):
        """Handle image upload process"""
        print("\n📷 의료 이미지 업로드")
        print("=" * 60)
        print("지원 형식: JPG, PNG, GIF, WebP")
        print("예시: X-ray, 피부 병변, CT 스캔 등")
        print()
        
        while True:
            path = input("이미지 파일 경로 (완료하려면 Enter): ").strip()
            if not path:
                break
            
            description = input("이미지 설명 (선택사항): ").strip()
            self.add_medical_image(path, description)
        
        if self.patient_info.images:
            print(f"\n✓ 총 {len(self.patient_info.images)}개 이미지 추가됨\n")
    
    def _conduct_inquiry(self):
        """Conduct structured medical inquiry (문진)"""
        if self.language == "ko":
            inquiry_system = """당신은 '진단의학과' 전문의입니다.
환자에게 정확한 진단을 위한 의학적 문진을 수행합니다.

규칙:
1. 질문은 반드시 한 번에 하나씩만 던집니다
2. 나이와 성별은 필수적으로 확인합니다
3. 만성 질환이나 복용 중인 약을 꼭 확인합니다
4. 필요시 가족력도 확인합니다
5. 증상을 구체적으로 파악합니다
6. 환자가 제공한 이미지가 있다면 그것을 참고하여 질문합니다

문진이 충분히 완료되었다고 판단되면 "문진 완료"라고 명확히 표시하세요."""
            
            greeting = "안녕하세요. 진단을 시작하겠습니다."
            first_msg = "환자가 방문했습니다. 첫 문진 질문을 시작하세요."
        else:
            inquiry_system = """You are a diagnostic medicine specialist.
You conduct medical inquiry to gather accurate diagnostic information.

Rules:
1. Ask only ONE question at a time
2. Age and gender are mandatory
3. Always check for chronic conditions and medications
4. Check family history when needed
5. Understand symptoms in detail
6. If patient provided images, refer to them in your questions

When inquiry is complete, clearly indicate "INQUIRY COMPLETE"."""
            
            greeting = "Hello. Let's begin the diagnosis."
            first_msg = "A patient has arrived. Start the first inquiry question."

        print(f"[진단의학과] {greeting}")
        
        # Show image count if any
        if self.patient_info.images:
            img_msg = f"({len(self.patient_info.images)}개 이미지 업로드됨)" if self.language == "ko" else f"({len(self.patient_info.images)} images uploaded)"
            print(f"           {img_msg}")
        
        # Initial question with images if available
        first_question, tool_info = self._call_claude(
            inquiry_system,
            first_msg,
            use_tools=self.enable_web_search,
            images=self.patient_info.images if self.patient_info.images else None
        )
        
        if tool_info:
            for tool in tool_info:
                if tool['name'] == 'web_search':
                    print(f"🔍 웹 검색: {tool['input'].get('query', '')}")
        
        print(f"[진단의학과] {first_question}")
        
        inquiry_context = f"이전 질문: {first_question}\n\n"
        
        while not self.inquiry_complete:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            # Update inquiry context
            inquiry_context += f"환자 답변: {user_input}\n\n"
            
            # Get next question with images
            next_prompt = f"{inquiry_context}환자의 답변을 바탕으로 다음 질문을 하거나, 충분한 정보를 얻었다면 '문진 완료'를 출력하세요." if self.language == "ko" else f"{inquiry_context}Based on the patient's answer, ask the next question or output 'INQUIRY COMPLETE' if sufficient information has been obtained."
            
            response, tool_info = self._call_claude(
                inquiry_system,
                next_prompt,
                use_tools=self.enable_web_search,
                images=self.patient_info.images if self.patient_info.images else None
            )
            
            # Show web search if used
            if tool_info:
                for tool in tool_info:
                    if tool['name'] == 'web_search':
                        print(f"🔍 웹 검색: {tool['input'].get('query', '')}")
            
            # Check for completion
            if "문진 완료" in response or "INQUIRY COMPLETE" in response:
                self.inquiry_complete = True
                completion_msg = "문진이 완료되었습니다. 전문의 선별 및 진단 토론을 시작합니다." if self.language == "ko" else "Inquiry complete. Starting specialist selection and diagnostic debate."
                print(f"\n[진단의학과] {completion_msg}\n")
                
                # Parse patient info from conversation
                self._parse_patient_info(inquiry_context + f"환자 답변: {user_input}")
                
                # Start diagnosis process
                self._start_diagnosis_debate()
                break
            else:
                print(f"[진단의학과] {response}")
                inquiry_context += f"질문: {response}\n\n"
    
    def _parse_patient_info(self, inquiry_text: str):
        """Parse patient information from inquiry conversation"""
        parse_system = """다음 문진 내용을 분석하여 환자 정보를 JSON 형식으로 추출하세요.

반드시 다음 형식으로 응답하세요:
{
    "age": 숫자 또는 null,
    "gender": "남성" 또는 "여성" 또는 null,
    "chronic_conditions": [질환 목록],
    "medications": [약물 목록],
    "family_history": [가족력 목록],
    "symptoms": [증상 목록]
}"""
        
        response, _ = self._call_claude(parse_system, inquiry_text)
        
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                patient_data = json.loads(json_match.group())
                self.patient_info.age = patient_data.get("age")
                self.patient_info.gender = patient_data.get("gender")
                self.patient_info.chronic_conditions = patient_data.get("chronic_conditions", [])
                self.patient_info.medications = patient_data.get("medications", [])
                self.patient_info.family_history = patient_data.get("family_history", [])
                self.patient_info.symptoms = patient_data.get("symptoms", [])
        except Exception as e:
            print(f"Warning: Could not parse patient info - {e}")
    
    def _start_diagnosis_debate(self):
        """Start the specialist selection and debate process"""
        # Step 1: Select specialists
        self._select_specialists()
        
        # Step 2: Form circular overlap groups
        self._form_circular_groups()
        
        # Step 3: Conduct debate
        self._conduct_debate()
        
        # Step 4: Present final diagnosis
        self._present_diagnosis()
    
    def _select_specialists(self):
        """Select optimal medical specialists based on symptoms"""
        selection_system = """당신은 진단의학과 전문의로서 환자의 증상을 분석하여 
필요한 전문의 과를 선별합니다.

환자 정보를 바탕으로 2-6개의 관련 전문과를 선택하세요.
형식: ["전문과1", "전문과2", ...]

예시 전문과: 내과, 신경과, 정형외과, 이비인후과, 안과, 피부과, 
정신건강의학과, 심장내과, 호흡기내과, 소화기내과, 영상의학과 등

이미지가 제공된 경우 이미지도 참고하여 전문과를 선별하세요."""

        patient_summary = f"""
나이: {self.patient_info.age}
성별: {self.patient_info.gender}
만성질환: {', '.join(self.patient_info.chronic_conditions) if self.patient_info.chronic_conditions else '없음'}
복용약물: {', '.join(self.patient_info.medications) if self.patient_info.medications else '없음'}
증상: {', '.join(self.patient_info.symptoms)}
업로드된 이미지: {len(self.patient_info.images)}개
"""
        
        response, tool_info = self._call_claude(
            selection_system, 
            patient_summary, 
            use_tools=self.enable_web_search,
            images=self.patient_info.images if self.patient_info.images else None
        )
        
        if tool_info:
            for tool in tool_info:
                if tool['name'] == 'web_search':
                    print(f"🔍 웹 검색: {tool['input'].get('query', '')}")
        
        try:
            import re
            # Extract list from response
            list_match = re.search(r'\[([^\]]+)\]', response)
            if list_match:
                specialists_str = list_match.group(1)
                self.selected_specialists = [s.strip(' "\'') for s in specialists_str.split(',')]
                print(f"선별된 전문과: {', '.join(self.selected_specialists)}\n")
        except Exception as e:
            print(f"Error selecting specialists: {e}")
            self.selected_specialists = ["내과", "신경과"]  # Fallback
    
    def _form_circular_groups(self):
        """Form circular overlap groups from selected specialists"""
        if len(self.selected_specialists) < 2:
            self.specialist_groups = [(self.selected_specialists[0], self.selected_specialists[0])]
            return
        
        # Create circular overlap: A+B, B+C, C+D, D+A
        for i in range(len(self.selected_specialists)):
            specialist_a = self.selected_specialists[i]
            specialist_b = self.selected_specialists[(i + 1) % len(self.selected_specialists)]
            self.specialist_groups.append((specialist_a, specialist_b))
        
        print("순환 중첩 그룹 구성:")
        for idx, (spec_a, spec_b) in enumerate(self.specialist_groups, 1):
            print(f"  그룹 {idx}: {spec_a} + {spec_b}")
        print()
    
    def _conduct_debate(self):
        """Conduct the 5-stage debate protocol with referee mediation"""
        print("=" * 80)
        print("진단 토론 시작 (내부 토론 과정은 생략, 최종 결과만 출력)")
        print("=" * 80)
        print()
        
        while self.current_round < self.max_rounds:
            self.current_round += 1
            
            # Check stagnation
            if self._check_stagnation():
                self._handle_stagnation()
                if self._should_terminate():
                    break
            
            # Run one complete debate cycle (5 stages)
            consensus_reached = self._run_debate_cycle()
            
            if consensus_reached:
                print(f"\n[Round {self.current_round}] 합의에 도달했습니다.\n")
                break
            
            # Check for max rounds
            if self.current_round >= self.max_rounds:
                print(f"\n[Round {self.current_round}] 최대 라운드 도달. 남은 이견을 병렬 출력합니다.\n")
                break
    
    def _run_debate_cycle(self) -> bool:
        """
        Run one complete cycle of the 5-stage debate
        
        Returns:
            True if consensus is reached, False otherwise
        """
        debate_system = f"""당신은 의학 전문의 토론 시스템의 일부입니다.

환자 정보:
나이: {self.patient_info.age}
성별: {self.patient_info.gender}
증상: {', '.join(self.patient_info.symptoms)}
만성질환: {', '.join(self.patient_info.chronic_conditions) if self.patient_info.chronic_conditions else '없음'}

현재 라운드: {self.current_round}

5단계 토론 프로토콜:
1. Opinion: 초기 진단 의견 제시
2. Referee Check: 근거 검증 및 환각 체크
3. Cross-Counter: 상호 반박
4. Rebuttal: 재반박
5. Final Judgment: 최종 판단

중립적 전문가 입장을 유지하고, 의학적 근거를 명확히 제시하세요."""

        # Stage 1: Opinion
        opinions = self._gather_opinions(debate_system)
        
        # Stage 2: Referee Check
        referee_feedback = self._referee_check(opinions)
        
        # Stage 3-4: Cross-Counter and Rebuttal
        rebuttals = self._cross_debate(opinions, referee_feedback)
        
        # Stage 5: Final Judgment
        consensus, final_opinions = self._final_judgment(rebuttals)
        
        self.active_opinions = final_opinions
        
        return consensus
    
    def _gather_opinions(self, system_prompt: str) -> List[DiagnosisOpinion]:
        """Stage 1: Gather initial opinions from specialist groups"""
        opinions = []
        
        for group_idx, (spec_a, spec_b) in enumerate(self.specialist_groups, 1):
            prompt = f"""그룹 {group_idx} ({spec_a} + {spec_b})로서 환자의 증상을 분석하고 
초기 진단 의견을 제시하세요.

제공된 이미지가 있다면 반드시 참고하세요.

다음 형식으로 응답:
진단명: [진단명]
확신도: [0-1 사이 숫자]
근거: [의학적 근거]
"""
            
            response, tool_info = self._call_claude(
                system_prompt, 
                prompt, 
                use_tools=self.enable_web_search,
                images=self.patient_info.images if self.patient_info.images else None
            )
            
            if tool_info:
                for tool in tool_info:
                    if tool['name'] == 'web_search':
                        print(f"  🔍 [{spec_a}+{spec_b}] 웹 검색: {tool['input'].get('query', '')}")
            
            # Parse response
            opinion = self._parse_opinion_response(f"{spec_a}+{spec_b}", response)
            opinions.append(opinion)
        
        return opinions
    
    def _parse_opinion_response(self, specialist: str, response: str) -> DiagnosisOpinion:
        """Parse opinion response into structured format"""
        import re
        
        diagnosis = "진단 미상"
        confidence = 0.5
        reasoning = response
        
        # Extract diagnosis
        diag_match = re.search(r'진단명:\s*(.+)', response)
        if diag_match:
            diagnosis = diag_match.group(1).strip()
        
        # Extract confidence
        conf_match = re.search(r'확신도:\s*([\d.]+)', response)
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
            except ValueError:
                pass
        
        # Extract reasoning
        reason_match = re.search(r'근거:\s*(.+)', response, re.DOTALL)
        if reason_match:
            reasoning = reason_match.group(1).strip()
        
        return DiagnosisOpinion(
            specialist=specialist,
            diagnosis=diagnosis,
            confidence=confidence,
            reasoning=reasoning
        )
    
    def _referee_check(self, opinions: List[DiagnosisOpinion]) -> str:
        """Stage 2: Referee validates opinions and checks for hallucinations"""
        referee_system = """당신은 의학 토론의 심판(Referee)입니다.

역할:
1. 제시된 진단 의견의 의학적 근거를 검증
2. 환각(hallucination) 또는 근거 없는 주장 탐지
3. 오류가 있는 의견에 대해 정정 명령
4. 모든 의견이 타당하면 승인

이미지 분석이 포함된 경우 영상 소견의 타당성도 검증하세요.
엄격하고 객관적으로 평가하세요."""

        opinions_text = "\n\n".join([
            f"[{op.specialist}]\n진단: {op.diagnosis}\n확신도: {op.confidence}\n근거: {op.reasoning}"
            for op in opinions
        ])
        
        feedback, tool_info = self._call_claude(
            referee_system,
            f"다음 진단 의견들을 검증하세요:\n\n{opinions_text}",
            use_tools=self.enable_web_search
        )
        
        if tool_info:
            for tool in tool_info:
                if tool['name'] == 'web_search':
                    print(f"  🔍 [심판] 웹 검색: {tool['input'].get('query', '')}")
        
        return feedback
    
    def _cross_debate(self, opinions: List[DiagnosisOpinion], referee_feedback: str) -> List[str]:
        """Stages 3-4: Cross-counter and rebuttal"""
        debate_system = f"""당신은 의학 전문의로서 다른 전문의의 의견에 대해 
교차 반박과 재반박을 수행합니다.

심판 피드백: {referee_feedback}

의학적 근거를 바탕으로 논리적으로 반박하거나 동의하세요."""

        rebuttals = []
        
        # Simplified cross-debate for efficiency
        for opinion in opinions:
            other_opinions = [op for op in opinions if op.specialist != opinion.specialist]
            if other_opinions:
                prompt = f"""당신의 의견: {opinion.diagnosis}

다른 의견들:
{chr(10).join([f"- {op.specialist}: {op.diagnosis}" for op in other_opinions])}

교차 반박을 수행하세요."""
                
                rebuttal, tool_info = self._call_claude(debate_system, prompt, use_tools=self.enable_web_search)
                rebuttals.append(rebuttal)
        
        return rebuttals
    
    def _final_judgment(self, rebuttals: List[str]) -> Tuple[bool, List[DiagnosisOpinion]]:
        """Stage 5: Referee makes final judgment on consensus"""
        referee_system = """당신은 심판으로서 토론을 종합하여 최종 판단을 내립니다.

합의 도달 조건:
- 모든 전문의가 동일하거나 매우 유사한 진단에 동의
- 근거가 충분하고 일관됨

합의 미도달 조건:
- 2개 이상의 상이한 진단이 남음
- 근거가 상충됨

판단 결과를 명확히 제시하세요:
"합의 도달: [진단명]" 또는 "합의 미도달: 남은 이견 [개수]"
"""

        rebuttals_text = "\n\n".join([f"재반박 {i+1}: {r}" for i, r in enumerate(rebuttals)])
        
        judgment, tool_info = self._call_claude(
            referee_system,
            f"다음 재반박들을 종합하여 최종 판단하세요:\n\n{rebuttals_text}",
            use_tools=self.enable_web_search
        )
        
        consensus = "합의 도달" in judgment
        
        return consensus, self.active_opinions
    
    def _check_stagnation(self) -> bool:
        """Check if debate has stagnated (10 rounds without progress)"""
        if len(self.active_opinions) == 0:
            return False
        
        current_opinions_str = "|".join(sorted([op.diagnosis for op in self.active_opinions]))
        
        if not self.last_opinions:
            self.last_opinions = [current_opinions_str]
            return False
        
        if current_opinions_str == self.last_opinions[-1]:
            self.stagnation_count += 1
        else:
            self.stagnation_count = 0
            self.last_opinions.append(current_opinions_str)
        
        return self.stagnation_count >= self.stagnation_threshold
    
    def _handle_stagnation(self):
        """Handle stagnation intervention"""
        print(f"\n[심판 개입] {self.stagnation_threshold}회 반복 감지. 개입을 시작합니다.\n")
        
        unique_opinions = len(set(op.diagnosis for op in self.active_opinions))
        
        if unique_opinions == 2:
            print("[심판] 2개의 유효 이견 존재. 토론을 종료하고 병렬 출력합니다.\n")
            self.current_round = self.max_rounds  # Force termination
        elif unique_opinions >= 3:
            print("[심판] 3개 이상의 이견 존재. 제3의 관점을 투입합니다.\n")
            self._inject_third_perspective()
    
    def _inject_third_perspective(self):
        """Inject a third perspective when stagnation occurs with 3+ opinions"""
        third_perspective_system = """당신은 토론에 새로운 관점을 제공하는 독립 전문의입니다.

기존 논의되지 않은 '제3의 관점'을 제시하여 토론을 진전시키세요.
기존 의견들의 맹점이나 간과된 가능성을 지적하세요."""

        current_opinions_text = "\n".join([
            f"- {op.specialist}: {op.diagnosis}" for op in self.active_opinions
        ])
        
        new_perspective, tool_info = self._call_claude(
            third_perspective_system,
            f"현재 의견들:\n{current_opinions_text}\n\n제3의 관점을 제시하세요.",
            use_tools=self.enable_web_search
        )
        
        if tool_info:
            for tool in tool_info:
                if tool['name'] == 'web_search':
                    print(f"  🔍 [독립전문의] 웹 검색: {tool['input'].get('query', '')}")
        
        # Add new perspective as an opinion
        new_opinion = DiagnosisOpinion(
            specialist="독립전문의",
            diagnosis="제3의 관점",
            confidence=0.7,
            reasoning=new_perspective
        )
        self.active_opinions.append(new_opinion)
        self.stagnation_count = 0  # Reset stagnation counter
    
    def _should_terminate(self) -> bool:
        """Check if debate should terminate"""
        return self.current_round >= self.max_rounds
    
    def _present_diagnosis(self):
        """Present final diagnosis results to the user"""
        print("=" * 80)
        print("최종 진단 결과")
        print("=" * 80)
        print()
        
        if len(self.active_opinions) == 0:
            print("진단을 완료할 수 없습니다. 추가 검사가 필요합니다.")
            return
        
        if len(self.active_opinions) == 1:
            opinion = self.active_opinions[0]
            print(f"[합의 진단]")
            print(f"진단명: {opinion.diagnosis}")
            print(f"확신도: {opinion.confidence:.2f}")
            print(f"근거: {opinion.reasoning}")
        else:
            print(f"[병렬 출력 - {len(self.active_opinions)}개의 가능 진단]")
            print()
            for idx, opinion in enumerate(self.active_opinions, 1):
                print(f"{idx}. [{opinion.specialist}]")
                print(f"   진단명: {opinion.diagnosis}")
                print(f"   확신도: {opinion.confidence:.2f}")
                print(f"   근거: {opinion.reasoning}")
                print()
        
        print("=" * 80)
        print("⚠️  면책조항: 이 시스템은 연구 목적으로 설계되었으며,")
        print("   전문 의료 진단을 대체할 수 없습니다.")
        print("   정확한 진단은 반드시 의료 전문가와 상담하세요.")
        print("=" * 80)


def main():
    """Main entry point for the diagnosis system"""
    print("\n" + "=" * 80)
    print("실시간 심판 개입 및 순환 중첩 구조 기반 고정밀 의료 진단 시스템")
    print("Real-time Referee-Mediated Medical Diagnosis System")
    print("=" * 80 + "\n")
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  ANTHROPIC_API_KEY=your-api-key-here")
        return
    
    try:
        system = MedicalDiagnosisSystem(api_key=api_key)
        system.start_diagnosis()
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
