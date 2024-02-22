import flask
from flask import request, jsonify
from llama_index.core import SimpleDirectoryReader, TreeIndex
import requests
import json
from openai import OpenAI
from llama_cpp import Llama
import os

app = flask.Flask(__name__, template_folder='./flask-environment/templates', static_folder='./flask-environment/static')
os.environ["OPENAI_API_KEY"] = "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"
upload_path = "./data/"


@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        # Elimina tutti i file nella cartella di upload
        filelist = [f for f in os.listdir(upload_path)]
        for f in filelist:
            os.remove(os.path.join(upload_path, f))
        return jsonify({'message': 'File eliminati con successo'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    # Removing all the files in the folder
    delete_files()

    if 'file' not in request.files:
        return jsonify({'error': 'Nessun file.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nessun file selezionato.'}), 400

    # Salvare il file nel percorso desiderato
    file.save(upload_path + file.filename)
    print("Done")

    return jsonify({'message': 'File caricati con successo!'}), 200


@app.route('/process', methods=['POST']) 
def process():  
    # Taking the question from the user
    data = flask.request.get_json()
    question = data['value']

    try:
        # Controlla se ci sono file nella cartella di upload
        files = os.listdir(upload_path)
        if files:
            documents = SimpleDirectoryReader("data").load_data(files[0])
            new_index = TreeIndex.from_documents(documents)

            query_engine = new_index.as_query_engine()
            response = query_engine.query(question)

            return jsonify({'result': str(response)}), 200
        else:
            # client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
            client = OpenAI()
            # Prompt for OpenAI
            messages = [
                {"role": "system", "content": "You are a compassionate and dedicated healthcare professional. Your priority is to provide accurate and helpful information while upholding ethical standards. Your responses should always promote positivity, respect, and safety. If a question is unclear or factually incorrect, kindly explain why rather than providing inaccurate information. If you're unsure of an answer, it's better to refrain from sharing false information. Answer to this questio:"
                },
                {"role": "user", "content": question},
                {"role": "system", "content":"Generates an answer relevant to the question only if related to the medical sector. If is not related to the medical sector, return the following answer: 'Sorry, but I am a medical chatbot, please ask me questions related to this field.'"
                }
            ]

            # Get the answer
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                max_tokens=100,
                temperature=0
            )

            # Extract the answer
            query = response.choices[0].message.content

            return jsonify({'result': str(query)}), 200

    except Exception as e:
        print(f"Errore: {str(e)}")
        print("ops")
        return None

    
@app.route('/')
def home():
    delete_files()
    return flask.render_template('home.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000, threaded=True, debug=True)