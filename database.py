import mysql.connector  # MySQL database connector
from mysql.connector import Error
import json      # For converting Python data to JSON format
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'gov_policy_rag'),
    'auth_plugin': 'mysql_native_password'
}


def get_connection():
    """
    Create and return a MySQL database connection.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print("\n💡 Try running this in MySQL command line:")
        print(f"   ALTER USER '{DB_CONFIG['user']}'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';")
        print(f"   FLUSH PRIVILEGES;")
        raise


def init_database():
    """
    STEP 1: Create the database and table (runs once when app starts)
    
    This function creates a table called 'Response_Table' to store:
    - User questions
    - Bot answers
    - Retrieved document chunks
    - Timing information
    """
    
    try:
        # Connect to MySQL server (without specifying database)
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create table if it doesn't already exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Response_Table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                user_query TEXT NOT NULL,
                llm_response TEXT NOT NULL,
                chunks_retrieved LONGTEXT NOT NULL,
                retrieval_time FLOAT NOT NULL,
                generation_time FLOAT NOT NULL,
                total_time FLOAT NOT NULL
            )
        ''')
        
        # Save changes and close connection
        conn.commit()
        conn.close()
        print("✓ MySQL database initialized successfully")
        
    except Error as e:
        print(f"✗ Error initializing database: {e}")
        raise

# =============================================================================
# SAVE DATA TO DATABASE
# =============================================================================

def store_response(user_query, llm_response, chunks, retrieval_time, generation_time):
    """
    STEP 2: Save a conversation to the database
    
    What this does:
    - Takes the user's question and bot's answer
    - Saves the document chunks that were used
    - Records how long everything took
    - Stores everything in one row in the database
    
    Simple example:
        store_response("What is policy X?", "Policy X is...", chunks, 0.5, 2.3)
    """
    
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()
        
        # STEP 2a: Extract chunk text and join with <break> separator
        chunks_data = "<stop>".join([chunk.page_content for chunk in chunks])
        
        # STEP 2b: Calculate total time
        total_time = retrieval_time + generation_time
        
        # STEP 2c: Get current date and time
        timestamp = datetime.now()
        
        # STEP 2d: Insert one new row into the table
        cursor.execute('''
            INSERT INTO Response_Table 
            (timestamp, user_query, llm_response, chunks_retrieved, retrieval_time, generation_time, total_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (timestamp, user_query, llm_response, chunks_data, retrieval_time, generation_time, total_time))
        
        # Get the ID of the row we just inserted
        record_id = cursor.lastrowid
        
        # Save changes and close connection
        conn.commit()
        conn.close()
        
        return record_id  # Return the ID so we can reference this record later
        
    except Error as e:
        print(f"Error storing response: {e}")
        return None

