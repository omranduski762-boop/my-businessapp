import streamlit as st
import pandas as pd
import os

# 1. دەرگەهێ پاسۆردی
def check_password():
    def password_entered():
        if st.session_state["password"] == "o.m.511": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("پاسۆردی بنڤیسە:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("پاسۆردی بنڤیسە:", type="password", on_change=password_entered, key="password")
        st.error("پاسۆرد هەلە!")
        return False
    else:
        return True

# 2. دەستپێکا سیستەمێ
if check_password():
    st.set_page_config(layout="wide", page_title="Shoes Pro System")

    st.markdown("""
        <style>
        .box-container { background-color: #e3f2fd; padding: 25px; border-radius: 20px; border: 2px solid #90caf9; margin-bottom: 20px; }
        .metric-card { background-color: #ffffff; padding: 15px; border-radius: 15px; border: 1px solid #bbdefb; margin: 5px; }
        h2, h4, p { color: #0d47a1 !important; }
        </style>
        """, unsafe_allow_html=True)

    FILE_NAME = "shoes_data.csv"

    def load_data():
        if os.path.exists(FILE_NAME): return pd.read_csv(FILE_NAME)
        else: return pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ'])

    if 'data' not in st.session_state: st.session_state.data = load_data()
    df = st.session_state.data

    # --- حسابکرنا داشبۆردێ ---
    stock_summary = df.groupby('مارکە')['کەمی'].sum().reset_index()
    
    st.markdown('<div class="box-container"><h2>📊 داشبۆرد و قازانج</h2>', unsafe_allow_html=True)
    
    # 3. پشکێ مەخزەن و قازانجی
    tab1, tab2, tab3, tab4 = st.tabs(["📦 مەخزەن و قازانج", "💰 فرۆتن", "➕ تومارکرن", "📊 ئامار"])

    with tab1:
        st.subheader("📦 لیستەیا مەخزەنی")
        for brand in stock_summary[stock_summary['کەمی'] > 0]['مارکە']:
            qty = stock_summary[stock_summary['مارکە'] == brand]['کەمی'].values[0]
            buy_price = df[(df['مارکە'] == brand) & (df['جۆر'] == 'کڕین')]['بها (IQD)'].iloc[-1]
            sell_price = df[(df['مارکە'] == brand) & (df['جۆر'] == 'فرۆتن')]['بها (IQD)'].iloc[-1] if not df[(df['مارکە'] == brand) & (df['جۆر'] == 'فرۆتن')].empty else 0
            profit = (sell_price - buy_price) if sell_price > 0 else 0
            
            st.markdown(f'''<div class="metric-card"><h4>👟 {brand}</h4>
            <p>کەمی: {qty} | <b>قازانجا هەر جوتەکێ: {profit:,.0f} IQD</b></p></div>''', unsafe_allow_html=True)

    with tab2:
        st.subheader("💰 تشتێن فرۆتی")
        st.dataframe(df[df['جۆر'] == 'فرۆتن'])

    with tab3:
        st.subheader("➕ تومارکرنا نوی")
        with st.form("add_form", clear_on_submit=True):
            brand = st.text_input("مارکە")
            qty = st.number_input("کەمی", min_value=1)
            price = st.number_input("بها (IQD)", min_value=0)
            op_type = st.selectbox("جۆر", ["کڕین", "فرۆتن"])
            if st.form_submit_button("تۆمار بکە 💾"):
                new_row = pd.DataFrame([[pd.Timestamp.now().date(), brand, (-qty if op_type == 'فرۆتن' else qty), price, (qty * price), op_type, 0]], 
                                       columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ'])
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True); st.session_state.data.to_csv(FILE_NAME, index=False); st.rerun()

    with tab4:
        if st.button("💾 دابەزاندنا داتایان (Backup)"):
            st.download_button("دابەزاندنا CSV", df.to_csv(index=False), "shoes_backup.csv", "text/csv")
        if st.button("🚨 ژێبرنا هەموو داتایان"):
            st.session_state.data = pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ']); st.session_state.data.to_csv(FILE_NAME, index=False); st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
