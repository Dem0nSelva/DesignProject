# app.py

import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

# Importing page modules
from main import show_analysis_page
from sentiment_overview import show_sentiment_overview
from terms_and_condition import show_social_effects
from chatbot import start_chatbot,show_chatbot_page
from authentication_page import authenticate_user, signup_user, get_db_connection

# Import home page function
from home_page import show_home_page

# Custom CSS for full-page background video and black-and-white color scheme
st.markdown("""
    <style>
        /* Make the entire webpage full-screen with a video background */
        .main {
            width: 100%;
            padding: 0;
            margin: 0;
        }

        /* Embed background video */
        body {
            background-color: black;
            color: white;
        }

        /* Fullscreen background video */
        #background-video {
            position: fixed;
            top: 0;
            left: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
            opacity: 0.4; /* Video transparency */
        }

        /* Black and white color scheme */
        h1 {
            font-size: 48px;
            color: black;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Buttons styling: black background with white text */
        .stButton button {
            background-color: black;
            color: white;
            border-radius: 5px;
            width: 200px;
            border: 1px solid white;
        }

        /* Align buttons in a single row */
        .stButton {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }

        /* Remove horizontal line below the title */
        hr {
            display: none;
        }
    </style>

    <!-- Background Video -->
    <video autoplay loop muted id="background-video">
        <source src="https://www.youtube.com/embed/QugooaNRnsk?autoplay=1&mute=1&loop=1&playlist=QugooaNRnsk" type="video/mp4">
        Your browser does not support the video tag.
    </video>
""", unsafe_allow_html=True)

# Custom function to display title with no line and centered
def display_custom_title():
    st.markdown("""
        <h1>📊 Sentiment Analysis App 📊</h1>
    """, unsafe_allow_html=True)

def main():


    # Initialize session state for user authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # If the user is not authenticated, show login/signup form
    if not st.session_state.authenticated:
        if 'signup_mode' not in st.session_state:
            st.session_state.signup_mode = False

        if st.session_state.signup_mode:
            st.subheader('Signup')
            new_email = st.text_input('New Email', key='new_email')
            new_password = st.text_input('New Password', type='password', key='new_password')
            if st.button('Signup'):
                if new_email and new_password:
                    signup_user(new_email, new_password)
                    st.success('Signup successful! You can now login.')
                else:
                    st.error('Please provide email and password.')
            if st.button('Back to Login'):
                st.session_state.signup_mode = False
                st.rerun()
        else:
            st.subheader('Login')
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            if st.button('Login'):
                if authenticate_user(email, password):
                    st.session_state.authenticated = True
                    st.success('Login successful!')
                    st.rerun()  # Rerun the app after login to load the pages
                else:
                    st.error('Incorrect email or password.')

            # Link for new users to create an account
            if st.button("Don't have an account? Create new"):
                st.session_state.signup_mode = True
                st.rerun()
    else:

        # Display navigation buttons below the title
        col1, col2, col3, col4 ,col5= st.columns([1, 1, 1, 1,1])

        if col1.button('Home'):
            st.session_state.page = 'Home'
        if col2.button('Sentiment Overview'):
            st.session_state.page = 'Sentiment Overview'
        if col3.button('Terms and Condition'):
            st.session_state.page = 'terms and condition'
        if col4.button('Sentiment Analysis'):
            st.session_state.page = 'Sentiment Analysis'
        if col5.button('Chatbot'):
            st.session_state.page = 'chatbot'

        # Set default page if no button was clicked
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'

        # Render the selected page
        if st.session_state.page == 'Home':
            show_home_page()
        elif st.session_state.page == 'Sentiment Overview':
            show_sentiment_overview()
        elif st.session_state.page == 'terms and condition':
            show_social_effects()
        elif st.session_state.page == 'Sentiment Analysis':
            with st.spinner('Processing sentiment analysis...'):
                result = show_analysis_page()
        elif st.session_state.page == 'chatbot':
            show_chatbot_page()
if __name__ == "__main__":
    main()
