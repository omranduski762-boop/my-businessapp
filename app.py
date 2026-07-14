import streamlit as st
import pandas as pd
import os

def check_password():
    def password_entered():
        if st.session_state["password"] == "12345": 
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
    if not os.path.exists(FILE_NAME):
        pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ']).to_csv(FILE_NAME, index=False)
    
    df = pd.read_csv(FILE_NAME)

    # --- داشبۆردێ ل سەری دابنێ ---
    st.markdown('<div class="box-container"><h2>📊 داشبۆرد و ئامار</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("کۆی پارچەیێن مایی", int(df['کەمی'].sum()))
    col2.metric("کۆی پارێ فرۆتنێ", f"{df[df['جۆر'] == 'فرۆتن']['کۆما گشتی'].sum():,.0f} IQD")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📦 مەخزەن و قازانج", "💰 فرۆتن", "➕ تومارکرن", "📊 ئامار"])

    with tab1:
        st.subheader("📦 لیستەیا مەخزەنی")
        summary = df.groupby('مارکە').agg({'کەمی': 'sum', 'بها (IQD)': 'last'}).reset_index()
        for _, row in summary.iterrows():
            if row['کەمی'] > 0:
                st.markdown(f'<div class="metric-card"><h4>👟 {row["مارکە"]}</h4><p>کەمی: {row["کەمی"]} | بها: {row["بها (IQD)"]:,.0f} IQD</p></div>', unsafe_allow_html=True)

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
                df = pd.concat([df, new_row], ignore_index=True); df.to_csv(FILE_NAME, index=False); st.rerun()

    with tab4:
        if st.button("💾 دابەزاندنا داتایان (Backup)"):
            st.download_button("دابەزاندنا CSV", df.to_csv(index=False), "shoes_backup.csv", "text/csv")
        if st.button("🚨 ژێبرنا هەموو داتایان"):
            pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ']).to_csv(FILE_NAME, index=False); st.rerun()
