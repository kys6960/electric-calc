# -*- coding: utf-8 -*-
"""
history.py — 월별 사용량 이력 저장/불러오기 모듈

확장 포인트:
- 저장 형식을 DB로 바꾸고 싶으면 이 파일만 수정
- 현재는 JSON 파일로 로컬 저장
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history() -> list:
    """저장된 이력 불러오기. 없으면 빈 리스트 반환."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_record(year: int, month: int, usage: int, total_bill: int, tier: int):
    """
    한 달치 데이터 저장.
    같은 년/월 데이터가 있으면 덮어씀.
    """
    history = load_history()

    # 기존 같은 월 데이터 제거
    history = [h for h in history if not (h["year"] == year and h["month"] == month)]

    history.append({
        "year": year,
        "month": month,
        "usage": usage,
        "total_bill": total_bill,
        "tier": tier,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

    # 년/월 순으로 정렬
    history.sort(key=lambda x: (x["year"], x["month"]))

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def delete_record(year: int, month: int):
    """특정 월 데이터 삭제."""
    history = load_history()
    history = [h for h in history if not (h["year"] == year and h["month"] == month)]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
