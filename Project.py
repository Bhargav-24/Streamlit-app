import streamlit as st

# Set page config with wide layout and custom title
st.set_page_config(page_title="Interactive Hackathon App", layout="wide")

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .stApp {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
        text-align: center;
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stSlider {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content
st.title("🚀 Interactive Hackathon App")
st.write("An engaging and colorful web app built with Streamlit!")

# User name input
name = st.text_input("Enter your name:", "")

if name:
    st.success(f"Welcome to our project, {name}! 🎉")

# Slider for interactivity
st.sidebar.header("🎨 Customize")
color_intensity = st.sidebar.slider("Select intensity:", 0, 100, 50)

# Button interaction
if st.button("Click Me!"):
    st.balloons()  # Fun effect

# Show slider value
st.write(f"Selected intensity: {color_intensity}")

# Footer
st.markdown("---")
st.markdown("Made with Streamlit")
