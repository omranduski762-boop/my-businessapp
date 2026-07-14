import streamlit as st
import pandas as pd
import os

# 1. دەرگەهێ پاسۆردی
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("پاسۆردی بنڤیسە:", type="password", key="password")
        if st.button("چوونە د ناڤ"):
            if st.session_state["password"] == "12345":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("پاسۆرد هەلە!")
        return False
    return st.session_state["password_correct"]

if check_password():
    st.set_page_config(layout="wide", page_title="Shoes Pro System")

    # CSS بۆ دیتنەکا جوان
    st.markdown("""
        <style>
        .box-container { background-color: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px solid #90caf9; }
        </style>
        """, unsafe_allow_html=True)

    FILE_NAME = "shoes_data.csv"
    if not os.path.exists(FILE_NAME):
        pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ']).to_csv(FILE_NAME, index=False)
    
    df = pd.read_csv(FILE_NAME)

    # --- حسابکرنا ئاماران ---
    total_qty = df['کەمی'].sum()
    total_sales = df[df['جۆر'] == 'فرۆتن']['کۆما گشتی'].sum()
    total_buy = df[df['جۆر'] == 'کڕین']['کۆما گشتی'].sum()
    profit = total_sales - total_buy

    # --- داشبۆرد ---
    st.markdown('<div class="box-container"><h2>📊 داشۆردا گشتی</h2>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("کۆی پارچە", int(total_qty))
    c2.metric("پارێ فرۆتنێ", f"{total_sales:,.0f}")
    c3.metric("پارێ کڕینێ", f"{total_buy:,.0f}")
    c4.metric("قازانجا گشتی", f"{profit:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📦 مەخزەن", "💰 فرۆتن", "➕ تومارکرن", "📊 ئامار"])

    with tab1:
        st.subheader("📦 لیستەیا مەخزەنی")
        st.dataframe(df.groupby('مارکە')['کەمی'].sum(), use_container_width=True)

    with tab2:
        st.subheader("💰 تشتێن فرۆتی")
        st.dataframe(df[df['جۆر'] == 'فرۆتن'], use_container_width=True)

    with tab3:
        with st.form("add_form", clear_on_submit=True):
            brand = st.text_input("مارکە")
            qty = st.number_input("کەمی", min_value=1)
            price = st.number_input("بها (IQD)")
            op_type = st.selectbox("جۆر", ["کڕین", "فرۆتن"])
            if st.form_submit_button("تۆمار بکە 💾"):
                f_qty = -qty if op_type == 'فرۆتن' else qty
                new_row = pd.DataFrame([[pd.Timestamp.now().date(), brand, f_qty, price, (qty * price), op_type, 0]], 
                                       columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ'])
                pd.concat([df, new_row], ignore_index=True).to_csv(FILE_NAME, index=False)
                st.rerun()

    with tab4:
        st.subheader("📊 ئامارێن زیندە")
        st.bar_chart(df.groupby('مارکە')['کەمی'].sum())
        if st.button("🚨 ژێبرنا هەموو داتایان"):
            pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'کۆما گشتی', 'جۆر', 'بهایێ کڕینێ']).to_csv(FILE_NAME, index=False); st.rerun()
