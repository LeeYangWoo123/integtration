import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

# 1. 페이지 설정
st.set_page_config(page_title="Pro Function Analyzer", layout="wide")

# 2. 다크 테마 전용 설정
bg_color = "#0D1117"
card_bg = "linear-gradient(145deg, #1e222d, #14171c)"
text_color = "#FFFFFF"
sub_text = "#8B949E"
input_bg = "#090C10"
btn_shadow = "5px 5px 10px #05070a, -2px -2px 10px #1d232d"
accent_blue = "#58A6FF"

# --- CSS 스타일 (다크 모드 고정) ---
st.markdown(f"""
<style>
    .main {{ background-color: {bg_color}; font-family: 'Inter', sans-serif; }}
    
    /* 텍스트 및 수식 스타일 */
    h1, h2, h3, label, p, .stMarkdown {{ color: {text_color} !important; }}
    .stLatex {{ color: {text_color} !important; font-size: 1.2em; }}

    /* 뉴모피즘 버튼 디자인 */
    .stButton > button {{
        width: 100% !important; height: 3.8em !important; border-radius: 16px !important;
        font-weight: 600 !important; color: {text_color} !important;
        background: {card_bg} !important; border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: {btn_shadow} !important; transition: all 0.2s ease; margin-bottom: 8px;
    }}
    
    .stButton > button:hover {{ 
        transform: translateY(-3px); 
        filter: brightness(1.2);
        border: 1px solid {accent_blue}55 !important;
    }}

    /* 버튼 타입별 포인트 컬러 */
    div[data-testid*="btn_op"] button {{ background: linear-gradient(145deg, #FF9F0A, #F78300) !important; color: #000 !important; border:none !important; }}
    div[data-testid*="btn_func"] button {{ background: linear-gradient(145deg, #007AFF, #0051FF) !important; color: #fff !important; border:none !important; }}
    div[data-testid*="btn_danger"] button {{ background: linear-gradient(145deg, #FF453A, #D70015) !important; color: #fff !important; border:none !important; }}

    /* 입력창 스타일 */
    div[data-baseweb="input"] {{
        background-color: {input_bg} !important;
        border: 1px solid #30363D !important;
        border-radius: 14px !important;
        padding: 5px !important;
    }}
    input {{ color: {accent_blue} !important; font-size: 1.5rem !important; font-weight: 600 !important; }}
</style>
""", unsafe_allow_html=True)

# 3. 로직 및 세션 관리
if "formula" not in st.session_state: st.session_state["formula"] = "x^2"
def insert_char(char): st.session_state["formula"] += str(char)
def clear_all(): st.session_state["formula"] = ""
def delete_last(): st.session_state["formula"] = st.session_state["formula"][:-1]

def convert_to_inverse():
    try:
        x, y = sp.symbols("x y")
        raw = st.session_state["formula"].replace("^", "**").replace("×", "*").replace("÷", "/")
        expr = parse_expr(raw, transformations=(standard_transformations + (implicit_multiplication_application,)))
        sol = sp.solve(sp.Eq(expr, y), x)
        if sol: st.session_state["formula"] = str(sol[0].subs(y, x)).replace("**", "^").replace(" ", "")
    except: st.toast("역함수 계산 불가")

# 4. UI 구성
st.title("📟 스마트 함수 분석기 PRO")

# 메인 입력창
st.text_input("수식 입력", key="formula")

pad_col, result_col = st.columns([1.3, 1.5], gap="large")

with pad_col:
    st.subheader("⌨️ 계산 패드")
    btn_layout = [
        [("x²", "^2", "op"), ("xⁿ", "^", "op"), ("√", "sqrt(", "func"), ("DEL", "del", "danger"), ("AC", "ac", "danger")],
        [("sin", "sin(", "func"), ("cos", "cos(", "func"), ("tan", "tan(", "func"), ("exp", "exp(", "func"), ("ln", "log(", "func")],
        [("7", "7", "num"), ("8", "8", "num"), ("9", "9", "num"), ("\\+", "+", "op"), ("\\-", "-", "op")],
        [("4", "4", "num"), ("5", "5", "num"), ("6", "6", "num"), ("×", "*", "op"), ("÷", "/", "op")],
        [("1", "1", "num"), ("2", "2", "num"), ("3", "3", "num"), ("(", "(", "num"), (")", ")", "num")],
        [("0", "0", "num"), (".", ".", "num"), ("x", "x", "op"), ("π", "pi", "num"), ("f⁻¹(x)", "inv", "danger")],
    ]
    for row in btn_layout:
        cols = st.columns(5)
        for i, (label, val, t_key) in enumerate(row):
            with cols[i]:
                k = f"btn_{t_key}_{label}_{i}"
                if val == "del": st.button(label, on_click=delete_last, key=k)
                elif val == "ac": st.button(label, on_click=clear_all, key=k)
                elif val == "inv": st.button(label, on_click=convert_to_inverse, key=k)
                else: st.button(label, on_click=insert_char, args=(val,), key=k)

with result_col:
    st.subheader("📊 분석 리포트")
    if st.session_state["formula"]:
        try:
            clean = st.session_state["formula"].replace("^", "**").replace("×", "*").replace("÷", "/").replace("π", "pi")
            x = sp.Symbol("x")
            expr = parse_expr(clean, transformations=(standard_transformations + (implicit_multiplication_application,)))
            
            # 1. LaTeX 메인 출력
            st.markdown(f"<div style='border-left: 4px solid {accent_blue}; padding-left: 15px;'><p style='color:{sub_text}; margin:0;'>주어진 함수</p></div>", unsafe_allow_html=True)
            st.latex(rf"f(x) = {sp.latex(expr)}")
            
            st.divider()

            # 2. 미분/적분 결과
            c1, c2 = st.columns(2)
            with c1:
                st.write("**📝 도함수**")
                st.latex(rf"f'(x) = {sp.latex(sp.diff(expr, x))}")
            with c2:
                st.write("**📝 부정적분**")
                st.latex(rf"\int f(x)dx = {sp.latex(sp.simplify(sp.integrate(expr, x)))} + C")

            # 3. 정적분 계산
            st.write("**🎯 구간 정적분**")
            ic1, ic2, ic3 = st.columns([1, 1, 1.2])
            with ic1: a = st.number_input("시작(a)", value=0.0)
            with ic2: b = st.number_input("끝(b)", value=1.0)
            with ic3: 
                res = sp.integrate(expr, (x, a, b))
                st.metric("Area Value", f"{float(res):.4f}")
            
            # 4. 그래프 시각화 (다크 모드 최적화)
            fig, ax = plt.subplots(figsize=(6, 3.2))
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor("#161B22")
            
            xr = np.linspace(a-3, b+3, 500); f_np = sp.lambdify(x, expr, "numpy")
            yr = f_np(xr)
            if isinstance(yr, (int, float)): yr = np.full_like(xr, yr)
            
            ax.plot(xr, yr, color=accent_blue, lw=2.5, zorder=3)
            ax.fill_between(xr, yr, where=((xr>=a)&(xr<=b)), color=accent_blue, alpha=0.25, zorder=2)
            
            # 축 및 그리드 설정
            ax.axhline(0, color="#484F58", lw=1)
            ax.axvline(0, color="#484F58", lw=1)
            ax.grid(True, linestyle=":", alpha=0.3, color="#8B949E")
            ax.tick_params(colors=sub_text, labelsize=8)
            for spine in ax.spines.values(): spine.set_edgecolor("#30363D")
            
            st.pyplot(fig)

        except: st.info("수식을 입력하고 버튼을 눌러보세요.")
