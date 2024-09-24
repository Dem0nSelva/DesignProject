import streamlit as st


# Assuming the start_chatbot function exists and takes two arguments
def start_chatbot(post, comments):
    st.write("Chatbot started...")
    # Your chatbot functionality for post and comments analysis will go here
    st.write(f"Analyzing post: {post}")
    st.write(f"Comments: {comments}")


def show_chatbot_page():
    # Initialize session state to control visibility of buttons
    if 'show_analyze_button' not in st.session_state:
        st.session_state.show_analyze_button = False

    st.subheader("Chatbot Sentiment Analysis")

    # Collect input from user for the post and comments
    post_input = st.text_area("Enter the post to analyze:")
    comments_input = st.text_area("Enter the comments (separated by new lines):")

    # Button to show the sentiment prediction button
    if st.button("Get Post and Comment Sentiment"):
        if post_input and comments_input:
            # After clicking "Get Post and Comment Sentiment", show sentiment analysis results
            comments_list = comments_input.split('\n')  # Split comments into list
            st.success("Sentiment prediction complete!")

            # Here, you can display predicted sentiment (placeholder for now)
            st.write("Post Sentiment: Positive")  # Placeholder for post sentiment analysis
            st.write("Comments Sentiment: Mixed")  # Placeholder for comments sentiment analysis

            # Show the next button to analyze the post and comments using the chatbot
            st.session_state.show_analyze_button = True
        else:
            st.error("Please provide both the post and comments.")

    # Button to analyze the post and comments using chatbot, appears only after the first button is clicked
    if st.session_state.show_analyze_button:
        if st.button("Analyze Post and Comments"):
            start_chatbot(post_input, comments_list)

