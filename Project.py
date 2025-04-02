import streamlit as st

# Set page config
st.set_page_config(page_title="Hackathon Project", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit branding
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Title and description
st.title("Hackathon Project")
st.write("Welcome to our Streamlit-based hackathon project!")

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.write("Use this panel to navigate.")

# Name input
name = st.text_input("Enter your name:")

# Display welcome message after input
if name:
    st.write(f"Welcome to our project, {name}!")

# Footer
st.write("---")
st.write("Made with Streamlit")
