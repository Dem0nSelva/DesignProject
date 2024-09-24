import streamlit as st
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error

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
        st.error(f"Error: {e}")
        return None

# User authentication
def authenticate_user(email, password):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            return True
        else:
            return False
    return False

# Signup user
def signup_user(email, password):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            st.error('Email already exists. Please log in.')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            st.success('Signup successful, please log in.')
        cursor.close()
        conn.close()
