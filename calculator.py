"""
calculator.py — 한전 가정용 전기 요금 계산 모듈
2024년 기준 누진제 요금 적용

확장 포인트:
- 새 요금 체계 반영 시 TIER_RATES 딕셔너리만 수정
- 산업용/농사용 추가 시 새 함수로 분리
"""

# ── 요금 테이블 (2024년 한전 기준) ───────────────────────────────

# 기본요금: 구간별 고정 요금
BASE_CHARGES = {
    "normal": {   # 주택용 저압
        1: 910,
        2: 1600,
        3: 7300,
    },
    "high": {     # 주택용 고압 (아파트 등)
        1: 730,
        2: 1260,
        3: 6060,
    }
}

# 누진 구간 경계 (kWh) — 여름(7~8월), 겨울(12~2월)은 완화
TIER_LIMITS = {
    "summer_winter": [200, 400],   # 7~8월, 12~2월
    "normal": [200, 400],           # 나머지 달 (동일, 향후 변경 대응용)
}

# 구간별 단가 (원/kWh)
UNIT_PRICES = {
    "normal": {   # 저압
        1: 112.0,
        2: 206.6,
        3: 299.3,
    },
    "high": {     # 고압
        1: 78.3,
        2: 147.3,
        3: 215.6,
    }
}

# 부가세율 및 전력산업기반기금
VAT_RATE = 0.10
FUND_RATE = 0.037


def _get_rate_type(household: str) -> str:
    """가구 유형 문자열 → 내부 요금 키 변환"""
    if "고압" in household:
        return "high"
    return "normal"


def _get_season(month: int) -> str:
    """월 → 시즌 분류"""
    if month in [7, 8, 12, 1, 2]:
        return "summer_winter"
    return "normal"


def get_tier_breakdown(usage: int, month: int, household: str = "일반 가구") -> list:
    """
    누진 구간별 사용량 분해.
    반환: [{"tier": 1, "used": kWh, "limit": kWh, "unit_price": 원}, ...]
    """
    rate_type = _get_rate_type(household)
    season = _get_season(month)
    limits = TIER_LIMITS[season]  # [200, 400]
    prices = UNIT_PRICES[rate_type]

    tier_limits = [limits[0], limits[1] - limits[0], float("inf")]
    remaining = usage
    result = []

    for i, cap in enumerate(tier_limits):
        tier_num = i + 1
        used = min(remaining, cap)
        result.append({
            "tier": tier_num,
            "used": int(used),
            "limit": int(cap) if cap != float("inf") else limits[1] + 9999,
            "unit_price": prices[tier_num],
        })
        remaining -= used
        if remaining <= 0:
            break

    # 사용 안 한 구간도 표시용으로 채우기
    while len(result) < 3:
        t = len(result) + 1
        result.append({
            "tier": t,
            "used": 0,
            "limit": 9999,
            "unit_price": prices[t],
        })

    return result


def calculate_bill(usage: int, month: int, household: str = "일반 가구") -> dict:
    """
    전기 요금 계산 메인 함수.
    반환: {total, base_charge, usage_charge, vat, fund, ...}
    """
    rate_type = _get_rate_type(household)
    season = _get_season(month)
    limits = TIER_LIMITS[season]
    prices = UNIT_PRICES[rate_type]
    base_table = BASE_CHARGES[rate_type]

    # 누진 구간 결정
    if usage <= limits[0]:
        tier = 1
    elif usage <= limits[1]:
        tier = 2
    else:
        tier = 3

    base_charge = base_table[tier]

    # 전력량 요금 계산
    usage_charge = 0
    tier_limits = [limits[0], limits[1] - limits[0], float("inf")]
    remaining = usage
    for i, cap in enumerate(tier_limits):
        tier_num = i + 1
        used = min(remaining, cap)
        usage_charge += used * prices[tier_num]
        remaining -= used
        if remaining <= 0:
            break

    usage_charge = int(usage_charge)
    subtotal = base_charge + usage_charge

    vat = int(subtotal * VAT_RATE)
    fund = int(subtotal * FUND_RATE)
    total = subtotal + vat + fund

    return {
        "total": total,
        "base_charge": base_charge,
        "usage_charge": usage_charge,
        "vat": vat,
        "fund": fund,
        "tier": tier,
        "subtotal": subtotal,
    }
