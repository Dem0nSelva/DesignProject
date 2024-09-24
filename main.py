import streamlit as st
import praw
from sentiment_analysis import analyze_sentiment

# Reddit API credentials
REDDIT_CLIENT_ID = 'G_g8iVFhdo18N_LoJ55h4g'
REDDIT_CLIENT_SECRET = 'dvic1ZE6m9rSzcD4SoMmkh4DZjvumg'
REDDIT_USER_AGENT = 'my_api/0'

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

def show_analysis_page():
    st.subheader('Sentiment Analysis')
    post_id = st.text_input('Enter Reddit Post ID:')
    if st.button('Get Post and Analyze Sentiment'):
        if post_id:
            try:
                submission = reddit.submission(id=post_id)
                post_text = submission.title + " " + submission.selftext
                st.subheader('Post:')
                st.write(post_text)

                # Get comments and analyze sentiment
                comments = submission.comments.list()
                comments_text = [comment.body for comment in comments if hasattr(comment, 'body')]
                if comments_text:
                    post_sentiment = analyze_sentiment([post_text])
                    comments_sentiment = analyze_sentiment(comments_text)
                    st.subheader('Post Sentiment:')
                    st.write(post_sentiment)
                    st.subheader('Comments Sentiment:')
                    st.write(comments_sentiment)
                else:
                    st.warning("No comments found for this post.")
            except Exception as e:
                st.error(f"Error fetching post: {e}")
