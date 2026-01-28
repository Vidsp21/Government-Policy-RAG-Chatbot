import sqlite3  # Built-in Python library for SQLite database
import json      # For converting Python data to JSON format
from datetime import datetime
from pathlib import Path

# =============================================================================
# DATABASE SETUP
# =============================================================================

# Where to save the database file (in the same folder as this script)
DB_PATH = Path(__file__).parent / "response_logs.db"


def init_database():
    """
    STEP 1: Create the database and table (runs once when app starts)
    
    This function creates a table called 'Response_Table' to store:
    - User questions
    - Bot answers
    - Retrieved document chunks
    - Timing information
    """
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Response_Table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_query TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            chunks_retrieved TEXT NOT NULL,
            retrieval_time REAL NOT NULL,
            generation_time REAL NOT NULL,
            total_time REAL NOT NULL
        )
    ''')
    
    # Save changes and close connection
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

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
    
    # Open connection to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # STEP 2a: Convert chunks to JSON format for storage
    # (We convert list of chunks into a text string)
    chunks_data = json.dumps([
        {
            "content": chunk.page_content,    # The actual text from the document
            "metadata": chunk.metadata         # Info like source file name
        }
        for chunk in chunks
    ])
    
    # STEP 2b: Calculate total time
    total_time = retrieval_time + generation_time
    
    # STEP 2c: Get current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Example: 2026-01-28 14:30:45
    
    # STEP 2d: Insert one new row into the table
    cursor.execute('''
        INSERT INTO Response_Table 
        (timestamp, user_query, llm_response, chunks_retrieved, retrieval_time, generation_time, total_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, user_query, llm_response, chunks_data, retrieval_time, generation_time, total_time))
    
    # Get the ID of the row we just inserted
    record_id = cursor.lastrowid
    
    # Save changes and close connection
    conn.commit()
    conn.close()
    
    return record_id  # Return the ID so we can reference this record later


# =============================================================================
# READ DATA FROM DATABASE
# =============================================================================

def get_all_responses():
    """
    Get ALL records from the database (newest first)
    Returns: List of all rows
    """
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all rows, sorted by newest first
    cursor.execute('SELECT * FROM Response_Table ORDER BY timestamp DESC')
    rows = cursor.fetchall()  # fetchall() gets all matching rows
    
    conn.close()
    return rows


def get_response_by_id(record_id):
    """
    Get ONE specific record by its ID number
    Example: get_response_by_id(5) returns record #5
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get one row where id matches
    cursor.execute('SELECT * FROM Response_Table WHERE id = ?', (record_id,))
    row = cursor.fetchone()  # fetchone() gets only one row
    
    conn.close()
    return row


def get_recent_responses(limit=10):
    """
    Get the most recent N records (default = 10)
    Example: get_recent_responses(5) returns last 5 records
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get limited number of rows, sorted by newest first
    cursor.execute('SELECT * FROM Response_Table ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def search_by_query(search_term):
    """
    Search for records where the user_query contains a word
    Example: search_by_query("policy") finds all queries about policies
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # The % signs mean "match anything before or after"
    # So "%policy%" matches "What is the policy?" or "Tell me policy details"
    cursor.execute('''
        SELECT * FROM Response_Table 
        WHERE user_query LIKE ? 
        ORDER BY timestamp DESC
    ''', (f'%{search_term}%',))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def get_database_stats():
    """
    Calculate statistics about all the records
    Returns a dictionary with:
    - How many total records
    - Average time for retrieval
    - Average time for generation
    - Average total time
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count total number of records
    cursor.execute('SELECT COUNT(*) FROM Response_Table')
    total_records = cursor.fetchone()[0]
    
    # Calculate average retrieval time
    cursor.execute('SELECT AVG(retrieval_time) FROM Response_Table')
    avg_retrieval = cursor.fetchone()[0] or 0  # If no data, use 0
    
    # Calculate average generation time
    cursor.execute('SELECT AVG(generation_time) FROM Response_Table')
    avg_generation = cursor.fetchone()[0] or 0
    
    # Calculate average total time
    cursor.execute('SELECT AVG(total_time) FROM Response_Table')
    avg_total = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Return results as a dictionary (easy to read)# Average generation time
    cursor.execute('SELECT AVG(generation_time) FROM Response_Table')
    avg_generation = cursor.fetchone()[0] or 0
    
    # Average total time
    cursor.execute('SELECT AVG(total_time) FROM Response_Table')
    avg_total = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total_records': total_records,
        'avg_retrieval_time': round(avg_retrieval, 3),
        'avg_generation_time': round(avg_generation, 3),
        'avg_total_time': round(avg_total, 3)
    }
