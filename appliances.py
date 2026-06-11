# -*- coding: utf-8 -*-
"""
appliances.py — 가전제품 소비전력 데이터 및 계산 모듈

확장 포인트:
- APPLIANCES 딕셔너리에 항목 추가하면 바로 앱에 반영
- 카테고리별로 분류되어 있어 UI 그룹핑 용이
"""

# ── 가전제품 소비전력 데이터 (단위: W) ──────────────────────────
APPLIANCES = {
    "냉방/난방": [
        {"name": "에어컨 (소형, 6~8평)", "watt": 900},
        {"name": "에어컨 (중형, 11~13평)", "watt": 1500},
        {"name": "에어컨 (대형, 15평 이상)", "watt": 2200},
        {"name": "전기장판 (중)", "watt": 80},
        {"name": "전기장판 (대)", "watt": 150},
        {"name": "온풍기", "watt": 1500},
        {"name": "전기히터", "watt": 1000},
    ],
    "주방": [
        {"name": "전기밥솥 (취사)", "watt": 900},
        {"name": "전기밥솥 (보온)", "watt": 40},
        {"name": "전자레인지", "watt": 1200},
        {"name": "인덕션 (1구)", "watt": 1400},
        {"name": "전기오븐", "watt": 2000},
        {"name": "냉장고 (소형)", "watt": 80},
        {"name": "냉장고 (대형)", "watt": 150},
        {"name": "식기세척기", "watt": 1200},
        {"name": "커피머신", "watt": 1000},
    ],
    "세탁/청소": [
        {"name": "세탁기 (일반)", "watt": 500},
        {"name": "드럼세탁기", "watt": 800},
        {"name": "건조기", "watt": 2000},
        {"name": "로봇청소기", "watt": 60},
        {"name": "진공청소기", "watt": 1000},
    ],
    "생활/엔터": [
        {"name": "TV 32인치", "watt": 60},
        {"name": "TV 55인치", "watt": 120},
        {"name": "TV 65인치 이상", "watt": 180},
        {"name": "데스크탑 PC", "watt": 300},
        {"name": "노트북", "watt": 60},
        {"name": "게이밍 PC", "watt": 600},
        {"name": "공기청정기", "watt": 50},
        {"name": "가습기", "watt": 30},
        {"name": "전기면도기 충전", "watt": 15},
    ],
    "욕실/위생": [
        {"name": "전기온수기 (순간식)", "watt": 3000},
        {"name": "헤어드라이어", "watt": 1500},
        {"name": "전기비데", "watt": 50},
    ],
}


def calc_appliance_kwh(watt: float, hours_per_day: float, days: int) -> float:
    """소비전력 → kWh 변환"""
    return round(watt * hours_per_day * days / 1000, 2)


def get_all_appliance_names() -> list:
    """전체 가전제품 이름 목록 반환 (카테고리 포함)"""
    result = []
    for category, items in APPLIANCES.items():
        for item in items:
            result.append(f"[{category}] {item['name']}")
    return result


def get_watt_by_name(display_name: str) -> int:
    """표시 이름으로 소비전력 반환"""
    for category, items in APPLIANCES.items():
        for item in items:
            full_name = f"[{category}] {item['name']}"
            if full_name == display_name:
                return item["watt"]
    return 0
