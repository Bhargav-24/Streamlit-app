import streamlit as st

# Configure the page settings
st.set_page_config(page_title="My Streamlit App", page_icon="🔥", layout="wide", initial_sidebar_state="collapsed")

# Hide extra Streamlit UI elements
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# App content
st.title("My First Streamlit App")
st.write("Hello, world! This is a web app using Streamlit.")

name = st.text_input("Enter your name:")
if st.button("Submit"):
    st.success(f"Hello, {name}! Welcome to Streamlit!")
