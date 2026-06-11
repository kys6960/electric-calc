# -*- coding: utf-8 -*-
import streamlit as st
from calculator import calculate_bill, get_tier_breakdown
from ai_engine import get_ai_advice
from history import load_history, save_record, delete_record
from charts import make_usage_chart, make_bill_chart
from appliances import APPLIANCES, calc_appliance_kwh, get_all_appliance_names, get_watt_by_name
from datetime import datetime

st.set_page_config(page_title="전기 요금 계산기", page_icon="⚡", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background-color: #0f1117; }
.hero { text-align: center; padding: 2.5rem 0 1.5rem 0; border-bottom: 1px solid #1e2230; margin-bottom: 2rem; }
.hero-label { font-size: 0.75rem; letter-spacing: 0.2em; color: #4a9eff; text-transform: uppercase; margin-bottom: 0.5rem; }
.hero-title { font-size: 2.2rem; font-weight: 700; color: #e8eaf0; letter-spacing: -0.02em; margin: 0; }
.hero-sub { font-size: 0.9rem; color: #5a6070; margin-top: 0.5rem; }
.card { background: #161b27; border: 1px solid #1e2536; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem; }
.card-title { font-size: 0.7rem; letter-spacing: 0.15em; color: #4a9eff; text-transform: uppercase; margin-bottom: 1rem; }
.bill-display { background: linear-gradient(135deg, #0d1f3c 0%, #132040 100%); border: 1px solid #1e4080; border-radius: 16px; padding: 2rem; text-align: center; margin: 1.5rem 0; }
.bill-kwh { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #4a9eff; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
.bill-amount { font-family: 'JetBrains Mono', monospace; font-size: 3rem; font-weight: 600; color: #ffffff; line-height: 1; }
.bill-unit { font-size: 1rem; color: #8892a4; margin-top: 0.3rem; }
.tier-bar-wrap { margin: 0.6rem 0; }
.tier-label { display: flex; justify-content: space-between; font-size: 0.78rem; color: #8892a4; margin-bottom: 0.25rem; }
.tier-bar-bg { background: #1e2536; border-radius: 4px; height: 8px; width: 100%; overflow: hidden; }
.tier-bar-fill { height: 8px; border-radius: 4px; }
.ai-box { background: #0d1f1a; border: 1px solid #1a3d2e; border-radius: 12px; padding: 1.5rem; color: #a0c8a0; font-size: 0.88rem; line-height: 1.75; white-space: pre-wrap; }
.ai-tag { font-size: 0.65rem; letter-spacing: 0.18em; color: #2ecc71; text-transform: uppercase; margin-bottom: 0.75rem; display: block; }

/* 가전 카드 */
.appliance-row { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #1e2536; font-size: 0.85rem; }
.appliance-name { color: #c8d0e0; }
.appliance-kwh { font-family: 'JetBrains Mono', monospace; color: #4a9eff; }
.appliance-cost { font-family: 'JetBrains Mono', monospace; color: #f39c12; }

/* 예측 결과 박스 */
.predict-box { background: linear-gradient(135deg, #1a0d2e 0%, #2a1040 100%); border: 1px solid #4a1e80; border-radius: 16px; padding: 2rem; text-align: center; margin: 1.5rem 0; }
.predict-before { font-size: 0.85rem; color: #8892a4; margin-bottom: 0.3rem; }
.predict-arrow { font-size: 1.5rem; color: #8892a4; margin: 0.5rem 0; }
.predict-after { font-family: 'JetBrains Mono', monospace; font-size: 2.8rem; font-weight: 600; color: #c084fc; line-height: 1; }
.predict-diff { font-size: 1rem; color: #f39c12; margin-top: 0.5rem; }

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label { color: #8892a4 !important; font-size: 0.85rem !important; }
.stButton > button { background: #1a4a8a; color: #ffffff; border: 1px solid #2260b0; border-radius: 8px; padding: 0.6rem 2rem; font-family: 'Noto Sans KR', sans-serif; font-weight: 600; font-size: 0.9rem; width: 100%; transition: all 0.2s; }
.stButton > button:hover { background: #2260b0; border-color: #4a9eff; }
.stTabs [data-baseweb="tab-list"] { background: #161b27; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #5a6070; border-radius: 8px; padding: 0.5rem 1.2rem; font-size: 0.88rem; }
.stTabs [aria-selected="true"] { background: #1a4a8a !important; color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-label">KEPCO · 한국전력 기준</div>
    <div class="hero-title">⚡ 전기 요금 계산기</div>
    <div class="hero-sub">가정용 누진제 요금 자동 계산 + 가전제품 예측 + 이력 관리</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚡ 요금 계산", "🏠 가전제품 예측", "📊 월별 이력"])

# ════════════════════════════════════════════
# TAB 1 — 요금 계산
# ════════════════════════════════════════════
with tab1:
    st.markdown('<div class="card"><div class="card-title">사용량 입력</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        usage = st.number_input("이번 달 사용량 (kWh)", min_value=0, max_value=2000, value=300, step=10)
    with col2:
        current_month = datetime.now().month
        month = st.selectbox("해당 월", options=list(range(1, 13)), index=current_month - 1,
                             format_func=lambda x: f"{x}월")
    year = st.selectbox("연도", options=[2023, 2024, 2025, 2026], index=3)
    household = st.selectbox("가구 유형", options=["일반 가구", "저압 (주택용 저압)", "고압 (아파트 고압)"])
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("요금 계산하기"):
        result = calculate_bill(usage, month, household)
        tiers = get_tier_breakdown(usage, month)
        st.session_state["result"] = result
        st.session_state["tiers"] = tiers
        st.session_state["calc_usage"] = usage
        st.session_state["calc_month"] = month
        st.session_state["calc_year"] = year
        st.session_state["saved"] = False

    if "result" in st.session_state:
        result = st.session_state["result"]
        tiers = st.session_state["tiers"]
        s_usage = st.session_state["calc_usage"]
        s_month = st.session_state["calc_month"]
        s_year = st.session_state["calc_year"]

        st.markdown(f"""
        <div class="bill-display">
            <div class="bill-kwh">{s_usage:,} kWh 사용</div>
            <div class="bill-amount">{result['total']:,}</div>
            <div class="bill-unit">원 (부가세·전력산업기반기금 포함)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">요금 구성</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("기본요금", f"{result['base_charge']:,}원")
            st.metric("전력량요금", f"{result['usage_charge']:,}원")
        with c2:
            st.metric("부가가치세", f"{result['vat']:,}원")
            st.metric("전력산업기반기금", f"{result['fund']:,}원")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">누진 구간 현황</div>', unsafe_allow_html=True)
        tier_colors = ["#4a9eff", "#f39c12", "#e74c3c"]
        tier_names = ["1구간 (저압)", "2구간 (중간)", "3구간 (고압)"]
        for i, tier in enumerate(tiers):
            if tier["limit"] > 0:
                pct = min(tier["used"] / tier["limit"] * 100, 100)
                st.markdown(f"""
                <div class="tier-bar-wrap">
                    <div class="tier-label">
                        <span>{tier_names[i]} — {tier['unit_price']}원/kWh</span>
                        <span>{tier['used']} / {tier['limit']} kWh</span>
                    </div>
                    <div class="tier-bar-bg">
                        <div class="tier-bar-fill" style="width:{pct}%; background:{tier_colors[i]};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get("saved"):
            st.success(f"✅ {s_year}년 {s_month}월 데이터가 저장됐어요!")
        else:
            if st.button(f"📥 {s_year}년 {s_month}월 데이터 저장하기"):
                save_record(s_year, s_month, s_usage, result['total'], result['tier'])
                st.session_state["saved"] = True
                st.rerun()

        st.markdown("---")
        st.markdown("### 💡 절약 조언")
        advice = get_ai_advice(s_usage, s_month, result['total'], tiers)
        st.markdown(f'<div class="ai-box"><span class="ai-tag">SAVING TIPS</span>{advice}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 2 — 가전제품 예측
# ════════════════════════════════════════════
with tab2:
    st.markdown("#### 현재 기준 사용량 설정")
    st.caption("가전제품을 추가하기 전, 현재 이번 달 사용량을 입력해주세요.")

    col1, col2 = st.columns(2)
    with col1:
        base_usage = st.number_input("현재 사용량 (kWh)", min_value=0, max_value=2000, value=300, step=10, key="ap_base")
    with col2:
        ap_month = st.selectbox("기준 월", options=list(range(1, 13)),
                                index=datetime.now().month - 1,
                                format_func=lambda x: f"{x}월", key="ap_month")

    st.markdown("---")
    st.markdown("#### 가전제품 추가")
    st.caption("추가하거나 더 사용할 가전제품을 선택해주세요.")

    # 가전제품 목록 (카테고리 구분선 포함)
    all_names = get_all_appliance_names()

    # session_state로 추가 목록 관리
    if "ap_list" not in st.session_state:
        st.session_state["ap_list"] = []

    # 추가 UI
    col_a, col_b, col_c, col_d = st.columns([3, 1.5, 1.5, 1])
    with col_a:
        selected = st.selectbox("가전제품 선택", options=all_names, key="ap_select")
    with col_b:
        hours = st.number_input("하루 사용시간 (h)", min_value=0.5, max_value=24.0, value=4.0, step=0.5, key="ap_hours")
    with col_c:
        days = st.number_input("사용일수", min_value=1, max_value=31, value=30, key="ap_days")
    with col_d:
        st.markdown("<div style='margin-top:1.6rem'>", unsafe_allow_html=True)
        if st.button("➕ 추가"):
            watt = get_watt_by_name(selected)
            kwh = calc_appliance_kwh(watt, hours, days)
            st.session_state["ap_list"].append({
                "name": selected.split("] ")[1],
                "watt": watt,
                "hours": hours,
                "days": days,
                "kwh": kwh,
            })
        st.markdown("</div>", unsafe_allow_html=True)

    # 추가된 가전제품 목록
    if st.session_state["ap_list"]:
        st.markdown("---")
        st.markdown("#### 추가된 가전제품 목록")

        total_added_kwh = 0
        rows_html = ""
        for i, ap in enumerate(st.session_state["ap_list"]):
            total_added_kwh += ap["kwh"]
            rows_html += f"""
            <div class="appliance-row">
                <span class="appliance-name">{'🔌 ' + ap['name']}</span>
                <span style="color:#5a6070; font-size:0.8rem">{ap['watt']}W × {ap['hours']}h × {ap['days']}일</span>
                <span class="appliance-kwh">+{ap['kwh']} kWh</span>
            </div>
            """

        st.markdown(f'<div class="card">{rows_html}</div>', unsafe_allow_html=True)

        # 전체 삭제 버튼
        if st.button("🗑 목록 초기화"):
            st.session_state["ap_list"] = []
            st.rerun()

        # ── 예측 결과 계산 ────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📈 요금 예측 결과")

        total_added_kwh = round(total_added_kwh, 1)
        new_usage = base_usage + total_added_kwh

        before = calculate_bill(base_usage, ap_month)
        after = calculate_bill(int(new_usage), ap_month)

        diff = after['total'] - before['total']
        diff_sign = "+" if diff >= 0 else ""
        diff_color = "#e74c3c" if diff > 0 else "#2ecc71"

        st.markdown(f"""
        <div class="predict-box">
            <div class="predict-before">현재 {base_usage} kWh → {before['total']:,}원</div>
            <div class="predict-arrow">＋ {total_added_kwh} kWh 추가 사용</div>
            <div style="font-size:0.85rem; color:#8892a4; margin-bottom:0.5rem">예상 총 사용량 {new_usage:.0f} kWh</div>
            <div class="predict-after">{after['total']:,}</div>
            <div class="bill-unit">원 (예상)</div>
            <div class="predict-diff" style="color:{diff_color}; margin-top:1rem; font-size:1.1rem">
                {diff_sign}{diff:,}원 {'증가 ⚠️' if diff > 0 else '감소 ✅'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 구간 변화 경고
        if after['tier'] > before['tier']:
            st.error(f"⚠️ 누진 구간이 {before['tier']}구간 → {after['tier']}구간으로 올라가요! 단가가 크게 오릅니다.")
        elif after['tier'] == before['tier']:
            st.info(f"✅ 현재와 동일한 {after['tier']}구간을 유지해요.")

        # 가전별 요금 기여도
        st.markdown("#### 가전별 요금 기여도")
        for ap in st.session_state["ap_list"]:
            ratio = (ap["kwh"] / total_added_kwh * 100) if total_added_kwh > 0 else 0
            approx_cost = int(ap["kwh"] * after["usage_charge"] / max(int(new_usage), 1))
            st.markdown(f"""
            <div class="appliance-row">
                <span class="appliance-name">🔌 {ap['name']}</span>
                <span class="appliance-kwh">{ap['kwh']} kWh ({ratio:.0f}%)</span>
                <span class="appliance-cost">약 {approx_cost:,}원</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem 0; color:#3a4050;">
            <div style="font-size:2rem; margin-bottom:0.5rem">🔌</div>
            <div style="color:#5a6070">위에서 가전제품을 추가해보세요</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 3 — 월별 이력
# ════════════════════════════════════════════
with tab3:
    history = load_history()

    if len(history) == 0:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📭</div>
            <div style="font-size: 1rem; color: #5a6070;">저장된 데이터가 없어요</div>
            <div style="font-size: 0.85rem; color: #3a4050; margin-top: 0.5rem;">요금 계산 후 "데이터 저장하기" 버튼을 눌러주세요</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_bills = [h["total_bill"] for h in history]
        total_usages = [h["usage"] for h in history]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("저장된 개월 수", f"{len(history)}개월")
        with c2:
            st.metric("평균 사용량", f"{sum(total_usages)//len(total_usages):,} kWh")
        with c3:
            st.metric("평균 요금", f"{sum(total_bills)//len(total_bills):,} 원")

        st.markdown("---")
        st.markdown("#### 📊 월별 사용량")
        st.plotly_chart(make_usage_chart(history), use_container_width=True)
        st.markdown("#### 💰 월별 요금")
        st.plotly_chart(make_bill_chart(history), use_container_width=True)

        st.markdown("#### 🗂 상세 내역")
        for h in reversed(history):
            col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 1])
            with col_a:
                st.write(f"**{h['year']}년 {h['month']}월**")
            with col_b:
                st.write(f"{h['usage']:,} kWh")
            with col_c:
                st.write(f"{h['total_bill']:,} 원")
            with col_d:
                if st.button("삭제", key=f"del_{h['year']}_{h['month']}"):
                    delete_record(h['year'], h['month'])
                    st.rerun()

st.markdown("""
---
<div style="text-align:center; color:#3a4050; font-size:0.75rem; padding: 1rem 0;">
    한전 2024년 기준 요금표 적용 · 실제 고지서와 소폭 차이가 있을 수 있어요
</div>
""", unsafe_allow_html=True)
