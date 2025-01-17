import streamlit as st

# 누진세율 기반 세액 계산
def calculate_income_tax(taxable_income):
    tax_brackets = [
        (12000000, 0.06, 0),
        (46000000, 0.15, 1080000),
        (88000000, 0.24, 5220000),
        (150000000, 0.35, 14900000),
        (300000000, 0.38, 19400000),
        (500000000, 0.40, 25400000),
        (float('inf'), 0.45, 35400000),
    ]
    for limit, rate, deduction in tax_brackets:
        if taxable_income <= limit:
            return taxable_income * rate - deduction

# 근로소득공제 계산
def calculate_work_income_deduction(total_income):
    if total_income <= 33000000:
        return total_income * 0.55
    elif total_income <= 70000000:
        return 7400000 - (total_income - 33000000) * 0.008
    elif total_income <= 120000000:
        return 5000000
    else:
        return 2000000

# 근로소득세액공제 계산
def calculate_work_tax_credit(calculated_tax):
    if calculated_tax <= 1300000:
        return calculated_tax * 0.55
    else:
        return 715000 + (calculated_tax - 1300000) * 0.3

# Streamlit 앱
st.title("연말정산 계산기")
st.write("국세청 연말정산 계산을 기반으로 한 예상 세액 계산기입니다.")

# 사용자 입력
total_income = st.number_input("총급여 (원):", min_value=0, step=1000000)
non_taxable_income = st.number_input("비과세소득 (원):", min_value=0, step=100000)
national_pension = st.number_input("국민연금보험료 (원):", min_value=0, step=100000)
health_insurance = st.number_input("건강보험료 (원):", min_value=0, step=100000)
credit_card_spending = st.number_input("신용카드 사용 금액 (원):", min_value=0, step=100000)
debit_cash_spending = st.number_input("체크카드/현금영수증 사용 금액 (원):", min_value=0, step=100000)
medical_expenses = st.number_input("의료비 지출 금액 (원):", min_value=0, step=100000)
donations = st.number_input("기부금 (원):", min_value=0, step=100000)
pension_saving = st.number_input("연금저축/IRP 납입 금액 (원):", min_value=0, step=100000)

# 계산 실행
if st.button("세액 계산"):
    # 과세 대상 총급여
    taxable_income_base = total_income - non_taxable_income

    # 근로소득공제
    work_income_deduction = calculate_work_income_deduction(taxable_income_base)

    # 기본 공제
    basic_deduction = 1500000 + (3 * 1500000)

    # 의료비 공제
    medical_deduction = max(0, medical_expenses - (taxable_income_base * 0.03)) * 0.15

    # 신용카드 공제
    card_limit = taxable_income_base * 0.25
    credit_card_deduction = max(0, credit_card_spending - card_limit) * 0.15
    debit_cash_deduction = max(0, debit_cash_spending - card_limit) * 0.30

    # 총 공제 금액
    total_deduction = (
        work_income_deduction + basic_deduction + medical_deduction +
        credit_card_deduction + debit_cash_deduction + national_pension + health_insurance
    )

    # 과세표준
    taxable_income = max(0, taxable_income_base - total_deduction)

    # 산출세액
    calculated_tax = calculate_income_tax(taxable_income)

    # 근로소득세액공제
    work_tax_credit = calculate_work_tax_credit(calculated_tax)

    # 결정세액
    final_tax = max(0, calculated_tax - work_tax_credit)

    st.write("### 계산 결과")
    st.write(f"💰 **총 공제 금액:** {total_deduction:,.0f} 원")
    st.write(f"📉 **과세표준:** {taxable_income:,.0f} 원")
    st.write(f"📊 **결정세액:** {final_tax:,.0f} 원")
