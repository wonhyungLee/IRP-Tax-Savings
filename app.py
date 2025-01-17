import streamlit as st

# 계산 함수
def calculate_tax(income, dependents, card_spending, medical_expenses, donations, pension_saving):
    # 기본 공제
    basic_deduction = 1500000 + (dependents * 1500000)
    
    # 신용카드 공제
    card_deduction = max(0, card_spending - (income * 0.25)) * 0.15

    # 의료비 공제
    medical_deduction = max(0, medical_expenses - (income * 0.03)) * 0.15

    # 기부금 공제
    donation_deduction = donations * 0.15

    # 연금저축/IRP 공제
    pension_deduction = min(pension_saving, 7000000) * 0.15

    # 총 공제 금액
    total_deduction = basic_deduction + card_deduction + medical_deduction + donation_deduction + pension_deduction

    # 결정세액 계산
    total_taxable_income = income - total_deduction
    tax = max(0, total_taxable_income * 0.15)

    return total_deduction, tax

# 조언 제공 함수
def provide_tips(income, dependents, card_spending, medical_expenses, donations, pension_saving):
    tips = []

    # 신용카드 공제 팁
    if card_spending < income * 0.25:
        tips.append("신용카드/체크카드 사용액이 총급여의 25%를 초과해야 공제가 가능합니다.")

    # 의료비 공제 팁
    if medical_expenses < income * 0.03:
        tips.append("의료비 공제는 총급여의 3%를 초과하는 지출에 대해서만 적용됩니다.")

    # 연금저축/IRP 공제 팁
    if pension_saving < 7000000:
        tips.append("연금저축과 IRP에 더 많이 납입하면 세액 공제를 최대 700만 원까지 받을 수 있습니다.")

    # 기부금 공제 팁
    if donations > 0:
        tips.append("기부금은 세액공제율 15%로 환급되며, 필요시 기부금 명세서를 제출하세요.")

    return tips

# Streamlit 앱
st.title("연말정산 세액 계산기")
st.write("입력한 정보를 바탕으로 예상 세액을 계산하고, 맞춤형 절세 팁을 제공합니다.")

# 사용자 입력
income = st.number_input("연간 총급여 (원):", min_value=0, step=1000000)
dependents = st.number_input("부양 가족 수 (본인 제외):", min_value=0, step=1)
card_spending = st.number_input("신용카드/체크카드/현금영수증 사용 금액 (원):", min_value=0, step=100000)
medical_expenses = st.number_input("의료비 지출 금액 (원):", min_value=0, step=10000)
donations = st.number_input("기부금 (원):", min_value=0, step=10000)
pension_saving = st.number_input("연금저축/IRP 납입 금액 (원):", min_value=0, step=100000)

# 계산 및 조언
if st.button("세액 계산 및 조언"):
    total_deduction, tax = calculate_tax(income, dependents, card_spending, medical_expenses, donations, pension_saving)
    tips = provide_tips(income, dependents, card_spending, medical_expenses, donations, pension_saving)

    st.write("### 계산 결과")
    st.write(f"💰 **총 공제 금액:** {total_deduction:,.0f} 원")
    st.write(f"📉 **예상 세액:** {tax:,.0f} 원")

    st.write("### 맞춤형 절세 팁")
    if tips:
        for tip in tips:
            st.write(f"- {tip}")
    else:
        st.write("🎉 모든 항목에서 최적의 공제를 받고 있습니다!")
