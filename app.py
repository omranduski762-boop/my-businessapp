import streamlit as st
import pandas as pd
import os

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

    FILE_NAME = "shoes_data.csv"
    if not os.path.exists(FILE_NAME):
        pd.DataFrame(columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'جۆر']).to_csv(FILE_NAME, index=False)
    
    df = pd.read_csv(FILE_NAME)

    # --- حسابکرنا دروست بۆ داشبۆردێ ---
    # کڕین: کەمی (+) | فرۆتن: کەمی (-)
    # کۆیا پارچەیێن مایی
    total_qty = df['کەمی'].sum()
    
    # کۆیێ پارێ فرۆتنێ
    total_sales = df[df['جۆر'] == 'فرۆتن']['بها (IQD)'].sum()
    
    # کۆیێ پارێ کڕینێ
    total_buy = df[df['جۆر'] == 'کڕین']['بها (IQD)'].sum()
    
    # قازانجا گشتی
    profit = total_sales - total_buy

    # داشبۆرد
    st.title("📊 داشۆردا گشتی")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("کۆی پارچەیێن مایی", int(total_qty))
    col2.metric("پارێ فرۆتنێ", f"{total_sales:,.0f} IQD")
    col3.metric("پارێ کڕینێ", f"{total_buy:,.0f} IQD")
    col4.metric("قازانجا گشتی", f"{profit:,.0f} IQD")
    
    st.markdown("---")

    # Tabs
    tab1, tab2 = st.tabs(["📦 مەخزەن و لیستە", "➕ تومارکرنا نوی"])

    with tab1:
        st.subheader("📦 لیستەیا مەخزەنی")
        st.dataframe(df, use_container_width=True)

    with tab2:
        with st.form("add_form"):
            b = st.text_input("مارکە")
            k = st.number_input("کەمی", step=1)
            p = st.number_input("بها (IQD)")
            j = st.selectbox("جۆر", ["کڕین", "فرۆتن"])
            if st.form_submit_button("تۆمار بکە"):
                # ئەگەر فرۆتن بیت، کەمی دێ بیتە نێگەتیڤ (-)
                final_k = -k if j == 'فرۆتن' else k
                new_row = pd.DataFrame([[pd.Timestamp.now().date(), b, final_k, p, j]], 
                                       columns=['مێژوو', 'مارکە', 'کەمی', 'بها (IQD)', 'جۆر'])
                new_row.to_csv(FILE_NAME, mode='a', header=False, index=False)
                st.success("هاتە تۆمارکرن!")
                st.rerun()
