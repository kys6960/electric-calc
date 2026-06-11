# ⚡ 전기 요금 계산기

한전 누진제 기준 가정용 전기 요금 자동 계산 + Claude AI 절약 조언

## 프로젝트 구조

```
electric_calc/
├── app.py          ← Streamlit UI (화면 담당)
├── calculator.py   ← 요금 계산 로직 (한전 누진제)
├── ai_engine.py    ← Claude API 호출 (AI 조언)
├── requirements.txt
└── README.md
```

## 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동으로 열려요.

## 향후 추가 가능한 기능

- [ ] 월별 사용량 이력 저장 및 그래프
- [ ] 가전제품별 소비전력 계산기
- [ ] 산업용 / 농사용 요금 지원
- [ ] 태양광 자가발전 상계 계산
- [ ] 요금 알림 설정

## 요금 기준

- 2024년 한전 주택용 전력 요금표 기준
- 저압 / 고압 구분 지원
- 계절별 누진 구간 반영 (7~8월, 12~2월 완화 적용)
