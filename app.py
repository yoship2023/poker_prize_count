import streamlit as st
import pandas as pd

def calculate_rtp(prize_pool, total_entry_fee):
    if total_entry_fee == 0:
        return 0
    return (prize_pool / total_entry_fee) * 100

def calculate_entries_for_rtp(entry_fee, rtp_target, total_prize):
    if rtp_target == 0:
        return 0
    prize_pool = total_prize / (rtp_target / 100 * entry_fee)
    return prize_pool

st.title("プライズかぞえチャオ")

# 入力フォーム
entry_fee = st.number_input("エントリー費用（円）", min_value=0, value=1000, step=1000)
num_entries = st.number_input("エントリー数", min_value=1, value=1)

# プライズ通貨の選択（ラジオボタン）
currency = st.radio("プライズ通貨を選択", ("ドル", "円"))
exchange_rate = st.number_input("1ドルのレート（円）", min_value=0.01 if currency == "ドル" else 0, value=140.0)

prize_pool_input = st.number_input("賞金総額", min_value=0, value=1)

# 賞金総額を円に変換
if currency == "ドル":
    prize_pool = prize_pool_input * exchange_rate
else:
    prize_pool = prize_pool_input

# エントリー費用の合計
total_entry_fee = entry_fee * num_entries

if st.button("還元率を計算"):
    rtp = calculate_rtp(prize_pool, total_entry_fee)
    st.success(f"プライズプールの合計は {total_entry_fee:} 円、還元率は {rtp:.2f} % です！")

    # 還元率ごとのエントリー数計算
    rtp_targets = [100, 90, 80, 70]
    entries_needed = [calculate_entries_for_rtp(entry_fee, rtp_target, prize_pool) for rtp_target in rtp_targets]

    # 結果を表形式で表示
    rtp_df = pd.DataFrame({
        "還元率 (%)": rtp_targets,
        "必要エントリー数": entries_needed
    })
    
    st.subheader("還元率ごとの必要エントリー数")
    st.table(rtp_df)
