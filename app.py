import streamlit as st
import pandas as pd

# دەرگەهێ پاسۆردی
def check_password():
    def password_entered():
        if st.session_state["password"] == "parezar511": 
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

# ئەگەر پاسۆرد درست بوو، سیستەمێ مخزنی کار دکەت
if check_password():
    st.title("bussnes.app")
    # ڤێرێ داتایێ بخوینە
    df = pd.read_csv('shoes_data.csv') 
    st.dataframe(df)
