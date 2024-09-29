from flask import Flask, request, jsonify, send_from_directory
import os
import fitz
from sentence_transformers import SentenceTransformer
from chromadb import Client
import signal
from groq import Groq

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = SentenceTransformer('all-MiniLM-L6-v2')
client = Client()
collection_name = "manual-cb"
collection = None

groq_client = Groq(api_key="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")

def groq_response(prompt):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model = "llama3-8b-8192"
    )

    return chat_completion.choices[0].message.content

def create_prompt(context, question):
    return f"Based on the following document: {context}\n\nAnswer the question: {question}"

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        return None

def chunk_text(text, chunk_size=500):
    sentences = text.split('. ')  # Split text into sentences
    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)
        if len(' '.join(current_chunk)) >= chunk_size:  # Adjust the chunk size here
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    # Append any remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global collection
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if collection is not None:
        client.delete_collection(name=collection_name)

    collection = client.create_collection(name=collection_name)

    text = extract_text(file_path)
    if text is None:
        return jsonify({'error': 'Unsupported file type'}), 400

    chunks = chunk_text(text)

    def embedding_function(inputs: list):
        return model.encode(inputs).tolist()

    embeddings = embedding_function(chunks)
    ids = [f"{file.filename}_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids  # Add all chunks with unique IDs
    )

    return jsonify({'message': 'File uploaded and processed successfully!'}), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    user_question = data.get('question')

    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    question_embedding = model.encode([user_question]).tolist()

    if collection is None:
        return jsonify({'answer': "Please upload a document first."}), 400
    
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=1
    )

    if results['documents']:
        main_chunk = results['documents'][0]
        
        query = create_prompt(main_chunk, user_question)
        answer = groq_response(query)
    else:
        answer = "I couldn't find an answer to your question."

    return jsonify({'answer': answer}), 200

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
