import streamlit as st

st.title("🛡️ 透明性100%・総額シミュレーター")

# 入力項目
price_man = st.number_input("表示価格（万円）", value=5000)
is_loan = st.checkbox("ローンを利用する", value=True)

# ロジック（乖離をなくすための詳細計算）
broker_fee = (price_man * 0.03 + 6) * 1.1
stamp_tax = 1.0 # 軽減税率（5000万クラス）
reg_tax = price_man * 0.015 # 概算
bank_fee = price_man * 0.022 if is_loan else 0 # ローン保証料等

total_overhead = broker_fee + stamp_tax + reg_tax + bank_fee
final_price = price_man + total_overhead

st.divider()

st.markdown(f"### 🏁 最終的な着地金額: **{final_price:.1f}万円**")
st.progress(price_man / final_price) # 総額に占める物件価格の割合を可視化

with st.expander("⚠️ なぜ表示金額より {total_overhead:.1f}万円 も増えるのか？"):
    st.write(f"- 仲介手数料: {broker_fee:.1f}万円")
    st.write(f"- 税金・登記費用: {stamp_tax + reg_tax:.1f}万円")
    if is_loan:
        st.write(f"- 銀行事務手数料・保証料: {bank_fee:.1f}万円")