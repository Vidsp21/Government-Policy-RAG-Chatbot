from flask import Flask, render_template, request, jsonify
from query.retriever import retrieve_context
from query.rag_chain import generate_answer
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question.strip():
            return jsonify({'error': 'Please enter a question'}), 400
        
        # Retrieve context
        start_time = time.time()
        docs = retrieve_context(question)
        retrieval_time = time.time() - start_time
        
        # Generate answer
        context = "\n\n".join([doc.page_content for doc in docs])
        generation_start = time.time()
        answer = generate_answer(context, question)
        generation_time = time.time() - generation_start
        
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
            'total_time': round(retrieval_time + generation_time, 2)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
