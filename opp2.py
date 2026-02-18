import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="Marathon 53km Achievement", page_icon="🏃‍♀️")

# タイトルとヘッダー
st.title("🏃‍♀️ 8-Day Marathon Challenge")
st.subheader("53.0km 目標達成おめでとうございます！")

# 実績データの作成
data = {
    "Day": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8"],
    "Distance (km)": [12.0, 0.0, 0.0, 21.0, 0.0, 5.0, 5.0, 10.0],
    "Activity": ["12km Run", "Trip", "Trip & Pilates", "21km Tempo Run", "Golf (100!)", "5km & Pilates", "5km & Study", "10km Goal!"]
}
df = pd.DataFrame(data)

# メトリクスの表示
col1, col2, col3 = st.columns(3)
col1.metric("Total Distance", f"{df['Distance (km)'].sum()} km", "Goal: 50km")
col2.metric("Longest Run", "21.0 km")
col3.metric("Golf Score", "99", "Best: 88")

# プログレスバー
progress = min(df['Distance (km)'].sum() / 50.0, 1.0)
st.write(f"Overall Progress: {int(progress * 100)}%")
st.progress(progress)

# チャートの表示
st.write("### Daily Progress Chart")
st.bar_chart(df.set_index("Day")["Distance (km)"])

# 詳細データ
st.write("### Activity Log")
st.table(df)

# コーチからのメッセージ
st.info("21km走の翌日にゴルフ100切り、そして最終日の10km完走。あなたの精神力と体力のマッシュアップは完璧です。木曜日の大阪出張も、このリズムで走り抜けましょう！")

# サイドバーにPythonコードを表示するおまけ
if st.sidebar.checkbox("Show Python Analysis"):
    st.sidebar.code("""
# 進捗計算ロジック
total = df['Distance (km)'].sum()
is_achieved = total >= 50
    """, language='python')