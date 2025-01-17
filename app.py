import streamlit as st

def calculate_optimal_strategy(rank, current_spending, prepaid_tax, target="zero_tax"):
    """
    교사 호봉 기반 최적 전략 계산
    :param rank: 호봉 (연봉 추정에 활용)
    :param current_spending: 현재 사용 내역 (딕셔너리 형태)
    :param prepaid_tax: 기납부 세액
    :param target: 목표 ("zero_tax" 또는 "refund_optimization")
    :return: 추천 전략
    """
    # 호봉을 기반으로 연봉 계산 (예: 1호봉당 300만 원 기준)
    total_income = rank * 3000000

    # 근로소득공제 계산
    if total_income <= 5000000:
        earned_income_deduction = total_income * 0.7
    elif total_income <= 15000000:
        earned_income_deduction = 3500000 + (total_income - 5000000) * 0.4
    elif total_income <= 45000000:
        earned_income_deduction = 7500000 + (total_income - 15000000) * 0.15
    else:
        earned_income_deduction = 12000000 + (total_income - 45000000) * 0.05

    # 과세표준 계산
    taxable_income = max(0, total_income - earned_income_deduction)

    # 소득세 계산 (구간별 세율 적용)
    if taxable_income <= 12000000:
        income_tax = taxable_income * 0.06
    elif taxable_income <= 46000000:
        income_tax = 12000000 * 0.06 + (taxable_income - 12000000) * 0.15
    elif taxable_income <= 88000000:
        income_tax = 12000000 * 0.06 + 34000000 * 0.15 + (taxable_income - 46000000) * 0.24
    else:
        income_tax = (
            12000000 * 0.06 + 34000000 * 0.15 + 42000000 * 0.24 + (taxable_income - 88000000) * 0.35
        )

    # 현재 공제 항목
    credit_card_deduction = current_spending.get("credit_card", 0) * 0.15
    debit_card_deduction = current_spending.get("debit_card", 0) * 0.3
    medical_deduction = current_spending.get("medical", 0) * 0.2
    donation_deduction = current_spending.get("donation", 0) * 0.15
    pension_deduction = current_spending.get("pension", 0) * 0.15

    # 총 공제액
    total_deductions = (
        credit_card_deduction + debit_card_deduction + medical_deduction +
        donation_deduction + pension_deduction + earned_income_deduction
    )

    # 결정세액 계산
    final_tax = max(0, income_tax - total_deductions - prepaid_tax)

    # 전략 추천
    recommendations = {}
    if target == "zero_tax":
        if final_tax > 0:
            additional_deductions_needed = final_tax / 0.15  # 대략적인 추가 공제 필요액 계산
            recommendations["pension"] = additional_deductions_needed  # 연금저축 납입 추천
        else:
            recommendations["status"] = "세액 0 달성"
    elif target == "refund_optimization":
        recommendations["credit_card"] = current_spending.get("credit_card", 0) * 1.1
        recommendations["pension"] = pension_deduction + 1000000  # 추가 연금저축 납입

    return final_tax, recommendations

# Streamlit 웹페이지 구성
st.title("교사 연말정산 최적 전략 추천기")
st.markdown("교사의 호봉과 현재 소비 내역을 입력하면 최적의 연말정산 전략을 추천합니다.")

# 사용자 입력 받기
st.sidebar.header("입력 항목")
rank = st.sidebar.number_input("교사 호봉 입력", min_value=1, step=1)
current_spending = {
    "credit_card": st.sidebar.number_input("신용카드 사용액 (원)", min_value=0, step=10000),
    "debit_card": st.sidebar.number_input("체크카드/현금영수증 사용액 (원)", min_value=0, step=10000),
    "medical": st.sidebar.number_input("의료비 지출액 (원)", min_value=0, step=10000),
    "donation": st.sidebar.number_input("기부금 지출액 (원)", min_value=0, step=10000),
    "pension": st.sidebar.number_input("연금저축/IRP 납입액 (원)", min_value=0, step=10000),
}

prepaid_tax = st.sidebar.number_input("기납부 세액 (원)", min_value=0, step=10000)

target = st.sidebar.selectbox("목표 선택", ["zero_tax", "refund_optimization"], format_func=lambda x: "세액 0 만들기" if x == "zero_tax" else "환급 최적화")

# 계산 버튼
if st.button("전략 계산하기"):
    final_tax, recommendations = calculate_optimal_strategy(rank, current_spending, prepaid_tax, target)

    # 결과 표시
    st.subheader("계산 결과")
    st.write(f"**결정세액:** {final_tax:,.0f}원")

    st.subheader("추천 전략")
    for key, value in recommendations.items():
        if key == "status":
            st.write(f"상태: {value}")
        else:
            st.write(f"{key}: {value:,.0f}원 추가")
