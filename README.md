# PDF Helper

PDF Helper is a Flask-based web application that allows users to upload PDF files, extract text from them, and ask questions about the content. The system uses the SentenceTransformer for embedding, a local vector database (ChromaDB) for managing document embeddings, and the Groq API for generating answers.

## Features

- **PDF Upload**: Upload and process PDF files.
- **Text Extraction**: Extract text from uploaded PDFs and chunk it into manageable segments.
- **Text Embedding**: Use SentenceTransformer to generate embeddings for the text chunks.
- **Question Answering**: Query the processed document and get answers using a language model via Groq API.

## Installation
### Prerequisites

- Python 3.9+
- Virtual environment setup (optional but recommended)

### Dependencies

- Flask
- Fitz (PyMuPDF)
- SentenceTransformers
- ChromaDB
- Groq

### Clone the Repository

```bash
git clone https://github.com/snithin2006/PDF-Helper.git
cd PDF-Helper
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Ensure you have the 'groq' Python package configured with your API key.

## Usage

### Running the Application

```bash
python app.py
```
The application will start on http://0.0.0.0:8080.

### Using the Application

1. Open your browser and navigate to 'http://localhost:8080'.
2. Use the upload feature to submit a PDF file.
3. After the PDF is processed, enter your question in the provided input field and submit.

### Application Flow

1. **Upload a PDF:** The user uploads a PDF document via the web interface.
2. **Text Extraction:** The application extracts the text and generates embeddings.
3. **Ask a Question:** The user can type a question about the document and receive an answer.

### Project Structure

1. **app.py:** Main application code.
2. **uploads/:** Directory where uploaded files are stored.
3. **static/:** Contains static files like index.html.

## Contact

For any questions or issues, please contact [nithin06.siva@gmail.com](mailto:nithin06.siva@gmail.com).
