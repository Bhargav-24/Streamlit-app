import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, world! This is a web app using Streamlit.")

name = st.text_input("Enter your name:")
if st.button("Submit"):
    st.success(f"Hello, {name}! Welcome to Streamlit!")
