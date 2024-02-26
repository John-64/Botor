from llama_index.core import SimpleDirectoryReader, TreeIndex
from flask import request, jsonify
from openai import OpenAI
import flask
import os


app = flask.Flask(__name__, template_folder='./flask-environment/templates', static_folder='./flask-environment/static')
os.environ["OPENAI_API_KEY"] = "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"
UPLOAD_PATH = "./data/"
memory = []


@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        filelist = [f for f in os.listdir(UPLOAD_PATH)]
        for f in filelist:
            os.remove(os.path.join(UPLOAD_PATH, f))
        return jsonify({'message': 'File eliminati con successo'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    delete_files()

    if 'file' not in request.files:
        return jsonify({'error': 'Nessun file inviato.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nome del file vuoto.'}), 400

    file.save(UPLOAD_PATH + file.filename)

    return jsonify({'message': 'File caricato con successo!'}), 200


@app.route('/process', methods=['POST']) 
def process():  
    data = flask.request.get_json()
    question = data['value']
    global memory

    try:
        files = os.listdir(UPLOAD_PATH)
        
        if files:
            documents = SimpleDirectoryReader("data").load_data(files[0])
            new_index = TreeIndex.from_documents(documents)

            prompt = "Answer the question that the user provides you. If the question is not related to at least of this categories: healthcare, medical, medicine, doctor, hospital, nursing, pharmaceutical, pharmaceuticals, therapy, therapist, surgery, surgeon, dentist, dental, psychiatrist, psychology, psychological, mental health, counseling and counselor, then reply: 'Please, only ask me questions related to the health sector."

            query_engine = new_index.as_query_engine(prompt=prompt)
            response = query_engine.query(question)

            return jsonify({'result': str(response)}), 200
        else:
            client = OpenAI()

            memory.append({"role": "system", "content": "Answer the question that the user provides you. if the question requires you to continue with the last prompt, continue to answer. If the question is not related to at least of this categories: healthcare, medical, medicine, doctor, hospital, nursing, pharmaceutical, pharmaceuticals, therapy, therapist, surgery, surgeon, dentist, dental, psychiatrist, psychology, psychological, mental health, counseling and counselor, then reply: 'Please, only ask me questions related to the health sector.'"})
            memory.append({"role": "user", "content": question})

            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-1106:personal::8vYWsgp1",
                messages=memory,
                temperature=0.2,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0.35,
                presence_penalty=0.35
            )

            response = str(completion.choices[0].message.content)

            memory.append({"role": "assistant", "content": response})

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

            print("####### Ecco la memoria:")
            print(memory)

            return jsonify({'result': response}), 200

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