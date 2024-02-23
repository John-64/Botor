from llama_index.core import SimpleDirectoryReader, TreeIndex
from flask import request, jsonify
from openai import OpenAI
import flask
import os


app = flask.Flask(__name__, template_folder='./flask-environment/templates', static_folder='./flask-environment/static')
os.environ["OPENAI_API_KEY"] = "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"
upload_path = "./data/"


@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        filelist = [f for f in os.listdir(upload_path)]
        for f in filelist:
            os.remove(os.path.join(upload_path, f))
        return jsonify({'message': 'File eliminati con successo'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    delete_files()

    if 'file' not in request.files:
        return jsonify({'error': 'Nessun file.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nessun file selezionato.'}), 400

    file.save(upload_path + file.filename)
    print("Done")

    return jsonify({'message': 'File caricati con successo!'}), 200


@app.route('/process', methods=['POST']) 
def process():  
    data = flask.request.get_json()
    question = data['value']

    try:
        files = os.listdir(upload_path)
        if files:
            documents = SimpleDirectoryReader("data").load_data(files[0])
            new_index = TreeIndex.from_documents(documents)

            query_engine = new_index.as_query_engine()
            response = query_engine.query(question)

            return jsonify({'result': str(response)}), 200
        else:
            client = OpenAI()
            
            messages = [
                {
                "role": "system",
                "content": "Answer the question that the user provides you and respond in a technical and precise manner to the medical sector"
                },
                {
                "role": "user",
                "content": question
                }
            ]

            # gpt-3.5-turbo-1106 - FineTuned
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-1106:personal::8vYWsgp1",
                messages=messages,
                temperature=0.2,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0.35,
                presence_penalty=0.35
            )

            
            """
            # gpt-3.5-turbo-1106
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                # model="gpt-4",
                messages=messages,
                max_tokens=100,
                temperature=0
            )
            """
            
            return jsonify({'result': str(completion.choices[0].message.content)}), 200

    except Exception as e:
        print(f"Errore: {str(e)}")
        return None

    
@app.route('/')
def home():
    delete_files()
    return flask.render_template('home.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9000, threaded=True, debug=True)