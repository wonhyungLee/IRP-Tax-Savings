import streamlit as st
import json

def calculate_tax(total_income, deductions, prepaid_tax):
    """
    연말정산 세액 계산 로직
    :param total_income: 총급여
    :param deductions: 공제 금액 (딕셔너리 형태)
    :param prepaid_tax: 기납부 세액
    :return: 결정세액과 환급 예상액
    """
    # 근로소득공제 계산
    if total_income <= 5000000:
        earned_income_deduction = total_income * 0.7
    elif total_income <= 15000000:
        earned_income_deduction = 3500000 + (total_income - 5000000) * 0.4
    elif total_income <= 45000000:
        earned_income_deduction = 7500000 + (total_income - 15000000) * 0.15
    else:
        earned_income_deduction = 12000000 + (total_income - 45000000) * 0.05

    # 총 공제금액
    total_deductions = sum(deductions.values()) + earned_income_deduction

    # 과세표준 계산
    taxable_income = max(0, total_income - total_deductions)

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

    # 결정세액 계산
    final_tax = max(0, income_tax - prepaid_tax)

    return final_tax, max(0, prepaid_tax - final_tax)

# Streamlit 웹페이지 구성
st.title("연말정산 세액 계산기")
st.markdown("총급여와 지출 내용을 입력하고 세액을 계산하세요.")

# 사용자 입력 받기
st.sidebar.header("입력 항목")
total_income = st.sidebar.number_input("총급여 (원)", min_value=0, step=10000)

prepaid_tax = st.sidebar.number_input("기납부 세액 (원)", min_value=0, step=10000)

# 각 공제 항목
deductions = {
    "신용카드 공제": st.sidebar.number_input("신용카드 사용액 (원)", min_value=0, step=10000),
    "체크카드/현금영수증 공제": st.sidebar.number_input("체크카드/현금영수증 사용액 (원)", min_value=0, step=10000),
    "의료비 공제": st.sidebar.number_input("의료비 지출액 (원)", min_value=0, step=10000),
    "기부금 공제": st.sidebar.number_input("기부금 지출액 (원)", min_value=0, step=10000),
    "연금저축/IRP 공제": st.sidebar.number_input("연금저축/IRP 납입액 (원)", min_value=0, step=10000),
}

# 계산 버튼
if st.button("세액 계산하기"):
    final_tax, refund = calculate_tax(total_income, deductions, prepaid_tax)

    # 결과 표시
    st.subheader("계산 결과")
    st.write(f"**결정세액:** {final_tax:,.0f}원")
    st.write(f"**환급 예상액:** {refund:,.0f}원")

    # 상세 계산 내역
    st.subheader("상세 계산 내역")
    st.write(f"총 공제액: {sum(deductions.values()):,.0f}원")
    for name, value in deductions.items():
        st.write(f"{name}: {value:,.0f}원")
