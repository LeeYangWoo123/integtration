# 파일 실행: python -m streamlit run app.py
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sympy.integrals.manualintegrate import integral_steps
from datetime import datetime

# 1. 페이지 설정 및 세션 초기화
st.set_page_config(page_title="AI 적분 분석기 PRO", layout="wide")

if 'formula' not in st.session_state:
    st.session_state.formula = "x**2 + cos(x)"
if 'history' not in st.session_state:
    st.session_state.history = []

def set_formula(new_f):
    st.session_state.formula = new_f

# 2. 사이드바 구성
st.sidebar.header("🎨 테마 및 공식")
theme_choice = st.sidebar.radio("그래프 모드", ["Dark Mode", "Light Mode"])

# 자주 쓰는 공식 버튼
st.sidebar.subheader("📚 공식 프리셋")
cols = st.sidebar.columns(2)
with cols[0]:
    if st.button("다항함수"): set_formula("x**3 - 2*x")
    if st.button("지수함수"): set_formula("exp(x)")
with cols[1]:
    if st.button("삼각함수"): set_formula("sin(x)")
    if st.button("복합함수"): set_formula("x * cos(x)")

st.sidebar.divider()
st.sidebar.header("⚙️ 계산 설정")
expr_input = st.sidebar.text_input("수식 입력 (Python 문법)", value=st.session_state.formula)
st.session_state.formula = expr_input

range_a = st.sidebar.number_input("구간 시작점 (a)", value=0.0)
range_b = st.sidebar.number_input("구간 끝점 (b)", value=2.0)

# 3. 메인 화면 로직
st.title("🌓 AI 적분 분석 및 시각화 대시보드")

try:
    x = sp.Symbol('x')
    expr = sp.sympify(st.session_state.formula)
    
    # [A] 실시간 프리뷰
    st.subheader("👀 수식 프리뷰")
    st.latex(rf"f(x) = {sp.latex(expr)}")
    st.divider()

    # [B] 계산 수행
    indefinite = sp.integrate(expr, x)
    definite = sp.integrate(expr, (x, range_a, range_b))
    definite_numeric = float(definite.evalf())

    # [C] 레이아웃 배치
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📝 계산 리포트")
        st.write("**부정적분 해:**")
        st.latex(rf"\int f(x) \, dx = {sp.latex(indefinite)} + C")
        
        st.write("**정적분 계산:**")
        st.latex(rf"\int_{{{range_a}}}^{{{range_b}}} f(x) \, dx = {definite_numeric:.4f}")
        st.metric("최종 수치 결과", f"{definite_numeric:.6f}")
        
        with st.expander("🔍 상세 풀이 단계 (Step-by-Step)"):
            try:
                steps = integral_steps(expr, x)
                st.code(steps)
            except:
                st.write("상세 단계 분석이 어려운 수식입니다.")

    with col2:
        st.subheader("📊 시각화 분석")
        
        # 테마 설정
        if theme_choice == "Dark Mode":
            plt.style.use('dark_background')
            bg_color = "#0E1117"
            text_color = "white"
        else:
            plt.style.use('default')
            bg_color = "white"
            text_color = "black"

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # 데이터 생성
        f_num = sp.lambdify(x, expr, 'numpy')
        x_plot = np.linspace(range_a - 1, range_b + 1, 400)
        y_plot = f_num(x_plot)
        
        ax.plot(x_plot, y_plot, color='#FF4B4B', lw=2.5, label='$f(x)$')
        ix = np.linspace(range_a, range_b, 100)
        ax.fill_between(ix, f_num(ix), color='#1C83E1', alpha=0.4, label='Area')
        
        ax.axhline(0, color=text_color, lw=1, alpha=0.3)
        ax.grid(True, linestyle='--', alpha=0.2)
        ax.legend(labelcolor=text_color)
        st.pyplot(fig)

    # [D] 히스토리 저장 및 관리
    st.divider()
    st.subheader("💾 계산 히스토리")
    
    if st.button("현재 결과 기록하기"):
        new_record = {
            "시간": datetime.now().strftime("%H:%M:%S"),
            "수식": st.session_state.formula,
            "구간": f"[{range_a}, {range_b}]",
            "결과": round(definite_numeric, 6)
        }
        st.session_state.history.append(new_record)

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.table(history_df)
        
        # CSV 다운로드
        csv = history_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📊 전체 기록 다운로드 (CSV)", csv, "integral_history.csv", "text/csv")

except Exception as e:
    st.error(f"⚠️ 입력 오류: {e}")
    st.info("Tip: 곱셈은 `*`, 거듭제곱은 `**` 기호를 사용하세요.")