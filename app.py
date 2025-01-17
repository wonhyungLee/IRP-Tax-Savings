import streamlit as st

# 세액공제 계산 함수
def calculate_tax_savings(investment, income):
    if income <= 55000000:  # 총급여 5,500만 원 이하
        rate = 0.15
    else:  # 총급여 5,500만 원 초과
        rate = 0.12
    savings = investment * rate
    return savings

# 미래 가치 계산 함수
def calculate_future_value(investment, rate, years):
    return investment * (1 + rate) ** years

# 웹페이지 제목
st.title("IRP 세액공제 및 투자 계산기")
st.write("IRP(개인형 퇴직연금)를 활용해 절감할 수 있는 세액과 미래 투자 수익을 계산해보세요.")

# 사용자 입력
income = st.number_input("연간 총급여를 입력하세요 (원):", min_value=0, step=100000)
investment = st.number_input("IRP 연간 납입 금액 (원):", min_value=0, step=100000)
rate = st.slider("예상 연 수익률 (%):", 0.0, 10.0, 5.0) / 100
years = st.number_input("투자 기간 (년):", min_value=1, step=1)

# 계산 결과
tax_savings = calculate_tax_savings(investment, income)
future_value = calculate_future_value(investment, rate, years)

# 결과 출력
st.write("### 계산 결과")
st.write(f"💰 **절감 가능한 세액:** {tax_savings:,.0f} 원")
st.write(f"📈 **{years}년 후 예상 자산 가치:** {future_value:,.0f} 원")

# 추가 설명
st.write("IRP를 활용하면 세제 혜택과 함께 장기적인 자산 관리를 효과적으로 할 수 있습니다. 지금 바로 시뮬레이션을 해보세요!")
