#!/usr/bin/env python
"""
=============================================================================
DATABASE VIEWER - View saved chatbot conversations
=============================================================================

This script lets you view all the queries and responses saved in the database.

What you can do:
1. See how many conversations are stored
2. View recent conversations
3. Search for specific topics
4. View detailed information about any conversation
"""

import json
from database import (
    get_all_responses,      # Get all records
    get_recent_responses,   # Get last N records
    search_by_query,        # Search for keyword
    get_database_stats,     # Get statistics
    get_response_by_id      # Get one specific record
)


def print_header():
    """Print the welcome message"""
    print("\n" + "="*80)
    print("📊 DATABASE VIEWER - View Your Chatbot Conversations")
    print("="*80)


def display_response(row, show_chunks=False):
    """
    Display one record in a nice format
    
    What this does:
    - Takes one row from the database
    - Prints it in an easy-to-read format
    - Optionally shows the document chunks that were used
    """
    
    # Check if we found a record
    if not row:
        print("❌ No record found.")
        return
    
    # Break down the row into individual pieces
    # (row is a tuple with 8 items)
    record_id = row[0]           # ID number
    timestamp = row[1]           # When it was asked
    user_query = row[2]          # User's question
    llm_response = row[3]        # Bot's answer
    chunks_retrieved = row[4]    # Document chunks (JSON string)
    retrieval_time = row[5]      # How long retrieval took
    generation_time = row[6]     # How long answer generation took
    total_time = row[7]          # Total time
    
    # Print everything nicely
    print(f"\n{'─'*80}")
    print(f"📝 Record ID: {record_id}")
    print(f"🕒 Date/Time: {timestamp}")
    print(f"\n❓ User Asked: {user_query}")
    print(f"\n💬 Bot Answered:\n{llm_response}")
    print(f"\n⏱️  Speed:")
    print(f"   • Retrieval took: {retrieval_time:.3f} seconds")
    print(f"   • Answer generation took: {generation_time:.3f} seconds")
    print(f"   • Total time: {total_time:.3f} seconds")
    
    # If user wants to see chunks, show them
    if show_chunks:
        # Convert JSON string back to Python list
        chunks = json.loads(chunks_retrieved)
        print(f"\n📚 Document Chunks Used ({len(chunks)} total):")
        
        # Show each chunk
        for i, chunk in enumerate(chunks, 1):
            print(f"\n  📄 Chunk {i}:")
            # Show first 200 characters of the chunk
            content_preview = chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content']
            print(f"  Text: {content_preview}")
            print(f"  Source: {chunk['metadata']}")
    
    print(f"{'─'*80}")


def show_stats():
    """Display summary statistics about the database"""
    stats = get_database_stats()
    
    print("\n📊 DATABASE STATISTICS:")
    print(f"   • Total conversations saved: {stats['total_records']}")
    print(f"   • Average retrieval time: {stats['avg_retrieval_time']:.3f} seconds")
    print(f"   • Average answer generation time: {stats['avg_generation_time']:.3f} seconds")
    print(f"   • Average total time: {stats['avg_total_time']:.3f} seconds")

def main_menu():
    """
    Main interactive menu
    
    This is the main program loop that shows options and gets user input
    """
    print_header()
    
    # Keep showing menu until user chooses to exit
    while True:
        # Show all available options
        print("\n\n📋 WHAT WOULD YOU LIKE TO DO?")
        print("─" * 40)
        print("1. 📊 View statistics (how many records, average times)")
        print("2. 🕒 View recent conversations (last 10)")
        print("3. 📚 View all conversations")
        print("4. 🔍 Search for specific topic")
        print("5. 🔢 View one specific record by ID")
        print("6. 🚪 Exit")
        print("─" * 40)
        
        # Get user's choice
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        # OPTION 1: Show statistics
        if choice == '1':
            show_stats()
        
        # OPTION 2: Show recent 10 records
        elif choice == '2':
            print("\n🕒 RECENT CONVERSATIONS:")
            rows = get_recent_responses(10)  # Get last 10
            
            if not rows:
                print("❌ No conversations found in database yet.")
            else:
                print(f"✓ Showing {len(rows)} most recent conversations:")
                for row in rows:
                    display_response(row, show_chunks=False)
        
        # OPTION 3: Show all records
        elif choice == '3':
            print("\n📚 ALL CONVERSATIONS:")
            rows = get_all_responses()  # Get everything
            
            if not rows:
                print("❌ No conversations found in database yet.")
            else:
                # Ask if user really wants to see all (might be a lot!)
                print(f"✓ Found {len(rows)} total conversations.")
                show_all = input(f"   Show all {len(rows)} records? (y/n): ").lower()
                
                if show_all == 'y':
                    for row in rows:
                        display_response(row, show_chunks=False)
                else:
                    # Just show first 5
                    print(f"\n✓ Showing first 5 conversations:")
                    for row in rows[:5]:
                        display_response(row, show_chunks=False)
        
        # OPTION 4: Search for keyword
        elif choice == '4':
            search_term = input("\n🔍 Enter word to search for: ").strip()
            
            if search_term:
                rows = search_by_query(search_term)
                
                if not rows:
                    print(f"❌ No conversations found with '{search_term}'")
                else:
                    print(f"\n✓ Found {len(rows)} conversations about '{search_term}':")
                    for row in rows:
                        display_response(row, show_chunks=False)
            else:
                print("❌ Please enter a search word.")
        
        # OPTION 5: View specific record by ID
        elif choice == '5':
            try:
                # Get ID number from user
                record_id = int(input("\n🔢 Enter Record ID number: ").strip())
                
                # Ask if they want to see chunks
                show_chunks = input("   Show document chunks? (y/n): ").lower() == 'y'
                
                # Get and display that record
                row = get_response_by_id(record_id)
                display_response(row, show_chunks=show_chunks)
                
            except ValueError:
                print("❌ Invalid ID. Please enter a number (like 1, 2, 3...).")
        
        # OPTION 6: Exit program
        elif choice == '6':
            print("\n👋 Goodbye! Thanks for using the database viewer!")
            break
        
        # Invalid choice
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 6.")


# =============================================================================
# START THE PROGRAM
# =============================================================================
if __name__ == "__main__":
    try:
        main_menu()  # Run the main menu
    except KeyboardInterrupt:
        # If user presses Ctrl+C, exit gracefully
        print("\n\n👋 Goodbye!")
    except Exception as e:
        # If something goes wrong, show the error
        print(f"\n❌ Error: {str(e)}")
