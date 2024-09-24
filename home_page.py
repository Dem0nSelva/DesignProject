# home_page.py

import streamlit as st


def show_home_page():
    st.title("Welcome to the Sentiment Analyzer!")
    st.markdown("""


        ### What is Sentiment Analysis?
        Sentiment analysis is a powerful tool that helps understand public opinion and sentiment trends. It analyzes text data from social media, reviews, and other sources to gauge positive, negative, or neutral sentiments.

        ### Key Features:
        - Real-time sentiment analysis of social media feeds.
        - Visualizations that show sentiment trends over time.
        - Impact analysis to understand social effects based on sentiment insights.

        ### Benefits:
        - Businesses can enhance customer satisfaction by responding to feedback.
        - Social media influencers can engage better by understanding audience reactions.
        - Researchers can analyze public sentiment on trending topics.

        ### How to Use:
        Watch our quick video tutorial to learn how to navigate the dashboard and leverage its features effectively.

        [Watch Tutorial Video](#)  <!-- Replace with your actual video link -->

        ### Visualize with Us:
        Explore our infographics and case studies to see how sentiment analysis drives actionable insights.

        <!-- Placeholder for Image -->
        ![Sentiment Analysis Image](https://via.placeholder.com/600x300.png?text=Sentiment+Analysis)

        ### Get Started:
        Sign up now to unlock more features and start analyzing sentiment today!

        ---

        #### Testimonials:
        *"The Sentiment Analysis Dashboard helped us understand customer sentiments quickly and make informed decisions." - Selva*

        #### Contact Us:
        Have questions or feedback? Contact our support team at [selvasheeba3085@gmail.com](mailto:selvasheeba3085@gmail.com).
    """)

    # Example of embedding a video using Streamlit
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with your actual video link

    # Example of displaying a sample chart using Streamlit
    import matplotlib.pyplot as plt
    import numpy as np

    chart_data = np.random.randn(20, 3)
    st.line_chart(chart_data)

    st.bar_chart(chart_data)


if __name__ == "__main__":
    show_home_page()
