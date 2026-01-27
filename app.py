from query.retriever import retrieve_context
from query.rag_chain import generate_answer_with_history

def main():
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
            # Retrieve relevant documents
            docs = retrieve_context(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate answer with conversation history
            answer = generate_answer_with_history(context, question, conversation_history)
            
            # Display answer
            print("\nBot:", answer)
            
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
