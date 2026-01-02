import streamlit as st

st.set_page_config(page_title="透明性100%・総額シミュレーター", layout="centered")

st.title("🛡️ 透明性100%・総額シミュレーター")
st.write("「表示価格」と「最終価格」の乖離をテックの力で解決します。")

# --- 入力セクション ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    price_man = st.number_input("物件の表示価格（万円）", value=5000, step=100)

with col_in2:
    is_loan = st.checkbox("住宅ローンを利用する", value=True)

# --- 計算ロジック ---
# 1. 仲介手数料 (3% + 6万) * 消費税1.1
broker_fee = (price_man * 0.03 + 6) * 1.1

# 2. 印紙代の計算
if price_man <= 5000:
    base_stamp = 1.0
elif price_man <= 10000:
    base_stamp = 3.0
else:
    base_stamp = 6.0

loan_stamp = 0.0
if is_loan:
    if price_man <= 5000:
        loan_stamp = 2.0
    elif price_man <= 10000:
        loan_stamp = 6.0
    else:
        loan_stamp = 10.0

stamp_tax = base_stamp + loan_stamp

# 3. 登録免許税・司法書士報酬の分解（修正箇所①）
reg_tax_only = price_man * 0.013  # 登録免許税のみ（概算1.3%）
judicial_scrivener_fee = 10.0    # 司法書士報酬（固定概算）
reg_tax_and_legal = reg_tax_only + judicial_scrivener_fee

# 4. 銀行費用
bank_fee = price_man * 0.022 if is_loan else 0.0

# 5. 合計諸費用の計算
total_overhead = broker_fee + stamp_tax + reg_tax_and_legal + bank_fee
final_price = price_man + total_overhead

# --- 表示セクション ---
st.divider()

st.markdown(f"### 🏁 最終的な着地金額（コミコミ）")
st.header(f"**{final_price:.1f} 万円**")

st.progress(price_man / final_price)
st.caption(f"内訳：物件価格 { (price_man/final_price)*100:.1f}% ／ 諸費用 { (total_overhead/final_price)*100:.1f}%")

with st.expander(f"⚠️ なぜ表示金額より 【{total_overhead:.1f}万円】 も増えるのか？"):
    st.write("日本の不動産取引では、物件価格以外に以下のコストが必ず発生します。")
    
    # 費用の内訳（修正箇所①：登記関連を分離）
    data = {
        "項目": ["仲介手数料 (税込)", "印紙税 (契約書2種合算)", "登録免許税 (税金)", "司法書士報酬", "銀行融資費用", "合計諸費用"],
        "概算金額": [
            f"{broker_fee:.1f} 万円",
            f"{stamp_tax:.1f} 万円",
            f"{reg_tax_only:.1f} 万円",
            f"{judicial_scrivener_fee:.1f} 万円",
            f"{bank_fee:.1f} 万円",
            f"**{total_overhead:.1f} 万円**"
        ]
    }
    st.table(data)
    
    # 注釈の復活（修正箇所②）
    st.info("※これに加え、固定資産税の日割り精算や火災保険料が別途発生します。")

# 中国人コミュニティ向け（人民元換算）
cny_rate = 0.05 
st.subheader(f"💴 人民元換算目安: 約 {(final_price * cny_rate):.2f} 万元")

st.divider()
if st.button("この見積もりをWeChatで担当者に送る"):
    st.success("WeChat用レポートの生成準備が完了しました。画面をスクリーンショットして送信してください。")
