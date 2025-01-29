import streamlit as st
import mysql.connector
from mysql.connector import connection
import pandas as pd
from datetime import datetime

# Database connection function
def get_database_connection():
    return connection.MySQLConnection(
        host='localhost',
        user='root',
        password='password',
        database='Grievances'
    )

# Initialize database tables
def init_db():
    db = get_database_connection()
    cursor = db.cursor()
    
    # Create users table
    create_users_table = '''
        CREATE TABLE IF NOT EXISTS USERS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(25) NOT NULL,
            password VARCHAR(25) NOT NULL
        )
    '''
    
    # Create complaints table
    create_complaints_table = '''
        CREATE TABLE IF NOT EXISTS COMPLAINTS(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            description TEXT,
            status VARCHAR(25),
            created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolution_desc VARCHAR(255) DEFAULT "Not Available",
            resolved_At TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    '''
    
    cursor.execute(create_users_table)
    cursor.execute(create_complaints_table)
    db.commit()
    cursor.close()
    db.close()

# User Authentication Functions
def register_user(username, password):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))
        db.commit()
        return True
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return False
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        select_query = "SELECT id FROM users WHERE username = %s AND password = %s"
        cursor.execute(select_query, (username, password))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        cursor.close()
        db.close()

# Complaint Management Functions
def submit_complaint(user_id, description):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        insert_query = "INSERT INTO complaints (user_id, description, status) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, description, "Pending"))
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        db.close()

def get_user_complaints(user_id):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        select_query = """
            SELECT id, description, status, created_At, resolution_desc, resolved_At 
            FROM complaints 
            WHERE user_id = %s
        """
        cursor.execute(select_query, (user_id,))
        columns = ['ID', 'Description', 'Status', 'Created At', 'Resolution', 'Resolved At']
        results = cursor.fetchall()
        return pd.DataFrame(results, columns=columns)
    finally:
        cursor.close()
        db.close()

def update_complaint_status(complaint_id, resolution_desc):
    db = get_database_connection()
    cursor = db.cursor()
    try:
        update_query = """
            UPDATE complaints 
            SET resolution_desc = %s, 
                status = 'Resolved', 
                resolved_At = CURRENT_TIMESTAMP 
            WHERE id = %s
        """
        cursor.execute(update_query, (resolution_desc, complaint_id))
        db.commit()
        return True
    finally:
        cursor.close()
        db.close()

# Streamlit UI
def main():
    st.set_page_config(page_title="Grievance Management System", layout="wide")
    
    # Initialize database
    init_db()
    
    # Session state initialization
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    st.title("Grievance Management System")
    
    # Login/Register sidebar
    with st.sidebar:
        st.header("Authentication")
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            if st.session_state.user_id is None:
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                if st.button("Login"):
                    user_id = login_user(login_username, login_password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            if st.session_state.user_id is None:
                reg_username = st.text_input("Username", key="reg_username")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                if st.button("Register"):
                    if register_user(reg_username, reg_password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed")
        
        if st.session_state.user_id is not None:
            if st.button("Logout"):
                st.session_state.user_id = None
                st.rerun()

    # Main content
    if st.session_state.user_id is not None:
        tab1, tab2, tab3 = st.tabs(["Submit Complaint", "View Complaints", "Update Complaint"])
        
        with tab1:
            st.header("Submit a New Complaint")
            complaint_text = st.text_area("Describe your complaint")
            if st.button("Submit"):
                if complaint_text.strip():
                    complaint_id = submit_complaint(st.session_state.user_id, complaint_text)
                    st.success(f"Complaint submitted successfully! Complaint ID: {complaint_id}")
                else:
                    st.warning("Please enter a complaint description")
        
        with tab2:
            st.header("Your Complaints")
            complaints_df = get_user_complaints(st.session_state.user_id)
            if not complaints_df.empty:
                st.dataframe(complaints_df, use_container_width=True)
            else:
                st.info("No complaints found")
        
        with tab3:
            st.header("Update Complaint Status")
            complaints_df = get_user_complaints(st.session_state.user_id)
            if not complaints_df.empty:
                complaint_id = st.selectbox("Select Complaint ID", complaints_df['ID'].tolist())
                resolution = st.text_area("Resolution Description")
                if st.button("Update Status"):
                    if update_complaint_status(complaint_id, resolution):
                        st.success("Complaint status updated successfully!")
                        st.rerun()
            else:
                st.info("No complaints to update")
    else:
        st.info("Please login or register to access the system")

if __name__ == "__main__":
    main()
