from query.retriever import retrieve_context
from query.rag_chain import generate_answer_with_history
import time
from datetime import datetime
from database import init_database, store_response

def main():
    # Initialize database on startup
    init_database()
    print("="*60)
    print("Government Policy Chatbot")
    print("="*60)
    print("Ask questions about government policies.")
    print("Type 'exit', 'quit', or 'q' to end the conversation.")
    print("Type 'clear' to reset conversation history.")
    print("="*60)
    print()
    
    conversation_history = []
    
    while True:
        # Get user question
        question = input("\n\nYou: ").strip()
        
        # Check for exit commands
        if question.lower() in ['exit', 'quit', 'q']:
            print("\nThank you for using the Government Policy Chatbot. Goodbye!")
            break
        
        # Check for clear history command
        if question.lower() == 'clear':
            conversation_history = []
            print("\n✓ Conversation history cleared.")
            continue
        
        # Skip empty questions
        if not question:
            print("Please enter a question.")
            continue
        
        try:
            retrieval_start = time.time()
            
            docs = retrieve_context(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            retrieval_end = time.time()
            retrieval_duration = retrieval_end - retrieval_start
            print(f"⏱️  Retrieval duration: {retrieval_duration:.3f} seconds")
            
            
            generation_start = time.time()
            
            answer = generate_answer_with_history(context, question, conversation_history)
            
            generation_end = time.time()
            generation_duration = generation_end - generation_start
            print(f"⏱️  Answer generation duration: {generation_duration:.3f} seconds")
            
            # Display answer
            print("\nBot:", answer)
            
            # Display total time
            total_duration = retrieval_duration + generation_duration
            print(f"\n{'='*60}")
            print(f"⏱️  TIMING SUMMARY:")
            print(f"   📊 Retrieval: {retrieval_duration:.3f}s | Generation: {generation_duration:.3f}s | Total: {total_duration:.3f}s")
            print(f"{'='*60}")
            
            # Store in database
            try:
                record_id = store_response(
                    user_query=question,
                    llm_response=answer,
                    chunks=docs,
                    retrieval_time=retrieval_duration,
                    generation_time=generation_duration
                )
                print(f"💾 Response saved to database (Record ID: {record_id})")
            except Exception as db_error:
                print(f"⚠️  Warning: Could not save to database: {str(db_error)}")
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": question})
            conversation_history.append({"role": "assistant", "content": answer})
            
            # Keep history manageable (last 10 exchanges = 20 messages)
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
                
        except Exception as e:
            print(f"\n Error: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()
