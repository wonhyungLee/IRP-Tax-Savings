import streamlit as st

def calculate_optimal_strategy(rank, prepaid_tax, target="zero_tax", selected_strategies=None):
    """
    교사 호봉 기반 최적 전략 계산
    :param rank: 호봉 (연봉 추정에 활용)
    :param prepaid_tax: 기납부 세액
    :param target: 목표 ("zero_tax", "refund_optimization")
    :param selected_strategies: 선택한 전략 (리스트)
    :return: 추천 전략
    """
    # 호봉별 봉급표 (2024년 기준)
    salary_table = {
        1: 1806700, 2: 1861400, 3: 1916900, 4: 1972200, 5: 2028000,
        6: 2083600, 7: 2138700, 8: 2194400, 9: 2249700, 10: 2285900,
        11: 2330600, 12: 2392600, 13: 2454400, 14: 2516500, 15: 2578500,
        16: 2819000, 17: 2883300, 18: 2947500, 19: 3011700, 20: 3265300,
        21: 3377600, 22: 3502000, 23: 3625800, 24: 3749800, 25: 3873600,
        26: 3997900, 27: 4127500, 28: 4256800, 29: 4386300, 30: 4515500,
        31: 4633100, 32: 4757200, 33: 4881900, 34: 5007200, 35: 5134600,
        36: 5246900, 37: 5364100, 38: 5464800, 39: 5582000, 40: 5821200
    }

    # 호봉을 기반으로 연봉 계산
    total_income = salary_table.get(rank, 0) * 12

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

    # 추천 전략 계산
    recommendations = {}
    if target == "zero_tax":
        if income_tax > prepaid_tax:
            additional_deductions_needed = (income_tax - prepaid_tax) / 0.15  # 대략적인 추가 공제 필요액 계산
            if selected_strategies:
                if "신용카드" in selected_strategies:
                    recommendations["신용카드 추천 사용액"] = additional_deductions_needed * 0.4
                if "체크카드" in selected_strategies:
                    recommendations["체크카드 추천 사용액"] = additional_deductions_needed * 0.3
                if "연금저축" in selected_strategies:
                    recommendations["연금저축 추천 납입액"] = additional_deductions_needed * 0.2
                if "의료비" in selected_strategies:
                    recommendations["의료비 추천 사용액"] = additional_deductions_needed * 0.1
                if "보험료" in selected_strategies:
                    recommendations["보험료 추천 납입액"] = additional_deductions_needed * 0.1
                if "기부금" in selected_strategies:
                    recommendations["기부금 추천 납입액"] = additional_deductions_needed * 0.1
        else:
            recommendations["status"] = "세액 0 달성"
    elif target == "refund_optimization":
        if selected_strategies:
            if "신용카드" in selected_strategies:
                recommendations["신용카드 추천 사용액"] = taxable_income * 0.15
            if "체크카드" in selected_strategies:
                recommendations["체크카드 추천 사용액"] = taxable_income * 0.3
            if "연금저축" in selected_strategies:
                recommendations["연금저축 추천 납입액"] = 1000000
            if "의료비" in selected_strategies:
                recommendations["의료비 추천 사용액"] = taxable_income * 0.1
            if "보험료" in selected_strategies:
                recommendations["보험료 추천 납입액"] = taxable_income * 0.1
            if "기부금" in selected_strategies:
                recommendations["기부금 추천 납입액"] = taxable_income * 0.1

    return income_tax, recommendations

# Streamlit 웹페이지 구성
st.title("교사 연말정산 최적 전략 추천기")
st.markdown("교사의 호봉을 입력하고 소비 전략을 체크박스로 선택하세요.")

# 사용자 입력 받기
st.sidebar.header("입력 항목")
rank = st.sidebar.number_input("교사 호봉 입력", min_value=1, max_value=40, step=1)
prepaid_tax = st.sidebar.number_input("기납부 세액 (원)", min_value=0, step=10000)

target = st.sidebar.selectbox(
    "목표 선택",
    ["zero_tax", "refund_optimization"],
    format_func=lambda x: "세액 0 만들기" if x == "zero_tax" else "환급 받기"
)

st.sidebar.header("세부 전략 선택")
selected_strategies = []
if st.sidebar.checkbox("신용카드"):
    selected_strategies.append("신용카드")
if st.sidebar.checkbox("체크카드"):
    selected_strategies.append("체크카드")
if st.sidebar.checkbox("연금저축"):
    selected_strategies.append("연금저축")
if st.sidebar.checkbox("의료비"):
    selected_strategies.append("의료비")
if st.sidebar.checkbox("보험료"):
    selected_strategies.append("보험료")
if st.sidebar.checkbox("기부금"):
    selected_strategies.append("기부금")

# 계산 버튼
if st.button("전략 계산하기"):
    final_tax, recommendations = calculate_optimal_strategy(rank, prepaid_tax, target, selected_strategies)

    # 결과 표시
    st.subheader("계산 결과")
    st.write(f"**결정세액:** {final_tax:,.0f}원")

    st.subheader("추천 전략")
    if not recommendations:
        st.write("선택된 항목이 없거나 추천할 전략이 없습니다.")
    else:
        for key, value in recommendations.items():
            if key == "status":
                st.write(f"상태: {value}")
            else:
                st.write(f"{key}: {value:,.0f}원")
