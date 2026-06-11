# -*- coding: utf-8 -*-
"""
charts.py — 그래프 생성 모듈

확장 포인트:
- 새 차트 추가 시 함수 하나 추가하고 app.py에서 호출
"""

import plotly.graph_objects as go

TIER_COLORS = {1: "#4a9eff", 2: "#f39c12", 3: "#e74c3c"}


def make_usage_chart(history: list) -> go.Figure:
    """월별 사용량 막대 그래프"""
    labels = [f"{h['year']}.{h['month']:02d}" for h in history]
    usages = [h["usage"] for h in history]
    colors = [TIER_COLORS.get(h["tier"], "#4a9eff") for h in history]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=usages,
        marker_color=colors,
        text=[f"{u}kWh" for u in usages],
        textposition="outside",
        textfont=dict(color="#8892a4", size=11),
        hovertemplate="%{x}<br>%{y} kWh<extra></extra>",
    ))

    # 누진 구간 기준선
    fig.add_hline(y=200, line_dash="dash", line_color="#4a9eff",
                  annotation_text="1구간 200kWh", annotation_font_color="#4a9eff",
                  annotation_position="top left")
    fig.add_hline(y=400, line_dash="dash", line_color="#e74c3c",
                  annotation_text="2구간 400kWh", annotation_font_color="#e74c3c",
                  annotation_position="top left")

    fig.update_layout(
        plot_bgcolor="#161b27",
        paper_bgcolor="#161b27",
        font_color="#8892a4",
        yaxis=dict(
            title="사용량 (kWh)",
            gridcolor="#1e2536",
            zerolinecolor="#1e2536",
        ),
        xaxis=dict(gridcolor="#1e2536"),
        margin=dict(t=30, b=20, l=20, r=20),
        showlegend=False,
        height=320,
    )
    return fig


def make_bill_chart(history: list) -> go.Figure:
    """월별 요금 꺾은선 그래프"""
    labels = [f"{h['year']}.{h['month']:02d}" for h in history]
    bills = [h["total_bill"] for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels,
        y=bills,
        mode="lines+markers+text",
        line=dict(color="#4a9eff", width=2),
        marker=dict(color="#4a9eff", size=8),
        text=[f"{b//1000}천원" for b in bills],
        textposition="top center",
        textfont=dict(color="#8892a4", size=11),
        fill="tozeroy",
        fillcolor="rgba(74,158,255,0.08)",
        hovertemplate="%{x}<br>%{y:,}원<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="#161b27",
        paper_bgcolor="#161b27",
        font_color="#8892a4",
        yaxis=dict(
            title="요금 (원)",
            gridcolor="#1e2536",
            zerolinecolor="#1e2536",
            tickformat=",",
        ),
        xaxis=dict(gridcolor="#1e2536"),
        margin=dict(t=30, b=20, l=20, r=20),
        showlegend=False,
        height=320,
    )
    return fig
