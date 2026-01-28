from flask import Flask, render_template, request, jsonify, session
from query.retriever import retrieve_context
from query.rag_chain import generate_answer_with_history
from database import init_database, store_response
import time
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Required for session support

# Initialize database on startup
init_database()

# Store conversation history per session
conversation_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        session_id = data.get('session_id', None)
        
        if not question.strip():
            return jsonify({'error': 'Please enter a question'}), 400
        
        # Create new session if not exists
        if not session_id or session_id not in conversation_sessions:
            session_id = secrets.token_hex(8)
            conversation_sessions[session_id] = []
        
        # Get conversation history for this session
        conversation_history = conversation_sessions[session_id]
        
        # Retrieve context
        start_time = time.time()
        docs = retrieve_context(question)
        retrieval_time = time.time() - start_time
        
        # Generate answer with history
        context = "\n\n".join([doc.page_content for doc in docs])
        generation_start = time.time()
        answer = generate_answer_with_history(context, question, conversation_history)
        generation_time = time.time() - generation_start
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Keep history manageable (last 10 exchanges = 20 messages)
        if len(conversation_history) > 20:
            conversation_sessions[session_id] = conversation_history[-20:]
        
        # Store in database
        try:
            record_id = store_response(
                user_query=question,
                llm_response=answer,
                chunks=docs,
                retrieval_time=retrieval_time,
                generation_time=generation_time
            )
            print(f"💾 Response saved to database (Record ID: {record_id})")
        except Exception as db_error:
            print(f"⚠️  Database error: {str(db_error)}")
        
        # Format source documents
        sources = []
        for i, doc in enumerate(docs, 1):
            sources.append({
                'index': i,
                'content': doc.page_content[:300] + '...' if len(doc.page_content) > 300 else doc.page_content,
                'metadata': doc.metadata
            })
        
        return jsonify({
            'answer': answer,
            'sources': sources,
            'retrieval_time': round(retrieval_time, 2),
            'generation_time': round(generation_time, 2),
            'total_time': round(retrieval_time + generation_time, 2),
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    try:
        data = request.get_json()
        session_id = data.get('session_id', None)
        
        if session_id and session_id in conversation_sessions:
            del conversation_sessions[session_id]
        
        return jsonify({'message': 'Conversation history cleared'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
