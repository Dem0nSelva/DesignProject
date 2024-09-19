from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error
import praw
from sentiment_analysis import analyze_sentiment

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Reddit API credentials
REDDIT_CLIENT_ID = 'G_g8iVFhdo18N_LoJ55h4g'
REDDIT_CLIENT_SECRET = 'dvic1ZE6m9rSzcD4SoMmkh4DZjvumg'
REDDIT_USER_AGENT = 'my_api/0'

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

# Database setup
def init_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='8006',
            database='selva'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                              id INT AUTO_INCREMENT PRIMARY KEY, 
                              email VARCHAR(255) UNIQUE NOT NULL, 
                              password VARCHAR(255) NOT NULL)''')
            connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

init_db()

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='8006',
            database='selva'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route for home (login page)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['login_email']
        password = request.form['login_password']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                if check_password_hash(user[2], password):
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
            else:
                flash('Email does not exist. Please sign up.', 'error')
            cursor.close()
            conn.close()
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['signup_email']
        password = request.form['signup_password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                flash('Email already exists. Please log in.', 'error')
            else:
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
                conn.commit()
                flash('Signup successful, please log in.', 'success')
                return redirect(url_for('home'))
            cursor.close()
            conn.close()
    return render_template('signup.html')

# Route for index (main page with sentiment analysis)
@app.route('/index')
def index():
    return render_template('index.html')

# Route to get Reddit post and comments
@app.route('/get_post_and_comments', methods=['POST'])
def get_post_and_comments():
    data = request.json
    post_id = data['post_id']

    try:
        submission = reddit.submission(id=post_id)
        post_text = submission.title + " " + submission.selftext
        comments = submission.comments.list()
        comments_text = [comment.body for comment in comments if hasattr(comment, 'body')]
        return jsonify({'post': post_text, 'comments': comments_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to analyze sentiment of post and comments
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    post_text = data['post']
    comments = data['comments']

    try:
        post_sentiment = analyze_sentiment([post_text])
        comments_sentiment = analyze_sentiment(comments)
        return jsonify({'post_sentiment': post_sentiment, 'comments_sentiment': comments_sentiment})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
