from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from llama_index.core import SimpleDirectoryReader, TreeIndex
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from flask import request, jsonify
from openai import OpenAI
import flask
import json
import os


with open("./config.json", "r") as c:
    config = json.load(c)

    API_KEY = config["OPENAI_KEY"]
    LLM_MODEL_NAME_FINE_TUNED = config["LLM_MODEL_NAME_FINE_TUNED"]
    LLM_MODEL_NAME = config["LLM_MODEL_NAME"]
    QDRANT_URL = config["QDRANT_URL"]
    EMBEDDING_NAME = config["EMBEDDING_NAME"]
    COLLECTION_NAME = config["COLLECTION_NAME"]
    QDRANT_URL = config["QDRANT_URL"]
    TEMPERATURE = config["TEMPERATURE"]
    MAX_TOKENS = config["MAX_TOKENS"]
    TOP_P = config["TOP_P"]
    FREQUENCY_PENALTY = config["FREQUENCY_PENALTY"]
    PRESENCE_PENALTY = config["PRESENCE_PENALTY"]


app = flask.Flask(__name__, template_folder='./flask-environment/templates', static_folder='./flask-environment/static')
os.environ["OPENAI_API_KEY"] = API_KEY
UPLOAD_PATH = "./data/"
patient = "None"
memory = []

def qdrant_load(collection_name):
    client = QdrantClient(url=QDRANT_URL, prefer_grpc=False)

    embeddings = HuggingFaceBgeEmbeddings(
        model_name=EMBEDDING_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    db = Qdrant(client=client, embeddings=embeddings, collection_name=collection_name)

    return db
    

@app.route('/delete-files', methods=['POST'])
def delete_files():
    try:
        filelist = [f for f in os.listdir(UPLOAD_PATH)]
        for f in filelist:
            os.remove(os.path.join(UPLOAD_PATH, f))
        return jsonify({'message': 'File eliminati con successo'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/selected_patient', methods=['POST'])
def selected_patient():
    global patient
    name_patient = request.form.get('patient_name')

    if name_patient != "None":
        patient = name_patient.replace(" ", "")
    else :
        patient = "None"
    return jsonify({'message': 'Paziente selezionato con successo'}), 200

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

            query_engine = new_index.as_query_engine(prompt="Answer the question that the user provides you. If the question is not related to healthcare, medical, medicine, doctor, hospital, nursing, pharmaceutical, pharmaceuticals, therapy, therapist, surgery, surgeon, dentist, dental, psychiatrist, psychology, psychological, mental health, counseling, counselor or other things releted to healtcare, then reply: 'Please, only ask me questions related to the health sector.")
            response = query_engine.query(question)

            return jsonify({'result': str(response)}), 200
        else:   
            client = OpenAI()

            if patient != "None":
                db_qdrant = qdrant_load(patient)

                docs = db_qdrant.similarity_search_with_score(query=question, k=20)

                analysis = []
                analysis.append({"role": "system", "content": "Analyze all this medical analysis and give me the general status of the patient."})   

                for i in docs:
                    doc, score = i
                    print({"score": score, "content": doc.page_content, "metadata": doc.metadata})
                    analysis.append({"role": "user", "content": doc.page_content})
                    analysis.append({"role": "assistant", "content": "Thanks for the analysis. Give me other analysis if you want."})

                completion = client.chat.completions.create(
                    model=LLM_MODEL_NAME,
                    messages=analysis,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    top_p=TOP_P,
                    frequency_penalty=FREQUENCY_PENALTY,
                    presence_penalty=PRESENCE_PENALTY
                )
                
                response = str(completion.choices[0].message.content)
                return jsonify({'result': response}), 200
            
            else:
                validation = [
                    {
                    "role": "system",
                    "content": "You are a helpful, respectful and honest medical assistant. So you have always answer as helpfully as possible, while being safe. Check if the question is related to at least of this categories: healthcare, medical, medicine, doctor, hospital, nursing, pharmaceutical, pharmaceuticals, therapy, therapist, surgery, surgeon, dentist, dental, psychiatrist, psychology, psychological, mental health, counseling, counselor or similar. If not, reply: 'Please, only ask me questions related to the health sector.'"
                    },
                    {
                    "role": "user",
                    "content": question
                    }
                ]
                
                completion = client.chat.completions.create(
                    model=LLM_MODEL_NAME,
                    messages=validation,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    top_p=TOP_P,
                    frequency_penalty=FREQUENCY_PENALTY,
                    presence_penalty=PRESENCE_PENALTY
                )

                response = str(completion.choices[0].message.content)

                if response != "Please, only ask me questions related to the health sector.":
                    db_qdrant = qdrant_load(COLLECTION_NAME)

                    docs = db_qdrant.similarity_search_with_score(query=question, k=1)
                    for i in docs:
                        doc, score = i
                        print({"score": score, "content": doc.page_content, "metadata": doc.metadata})
                    
                    if score > 0.85:
                        memory.append({"role": "system", "content": "If the context of the following information is related to the question, use this information by rephrasing the answer completely and adding missing information, otherwise ignore it and answer on your own, always respecting the system prompt: " + str(doc.page_content)})
                        memory.append({"role": "user", "content": question})

                        completion = client.chat.completions.create(
                            model=LLM_MODEL_NAME_FINE_TUNED,
                            messages=memory,
                            temperature=TEMPERATURE,
                            max_tokens=MAX_TOKENS,
                            top_p=TOP_P,
                            frequency_penalty=FREQUENCY_PENALTY,
                            presence_penalty=PRESENCE_PENALTY
                        )
                        
                        response = str(completion.choices[0].message.content)
                        memory.append({"role": "assistant", "content": response})
                    else:
                        memory.append({"role": "system", "content": "Answer the question that the user provides you. if the question requires you to continue with the last prompt, continue to answer. If the question is not related to at least of this categories: healthcare, medical, medicine, doctor, hospital, nursing, pharmaceutical, pharmaceuticals, therapy, therapist, surgery, surgeon, dentist, dental, psychiatrist, psychology, psychological, mental health, counseling and counselor, then reply: 'Please, only ask me questions related to the health sector.'"})   
                        memory.append({"role": "user", "content": question})

                        completion = client.chat.completions.create(
                            model=LLM_MODEL_NAME_FINE_TUNED,
                            messages=memory,
                            temperature=TEMPERATURE,
                            max_tokens=MAX_TOKENS,
                            top_p=TOP_P,
                            frequency_penalty=FREQUENCY_PENALTY,
                            presence_penalty=PRESENCE_PENALTY
                        )
                        
                        response = str(completion.choices[0].message.content)
                        
                        memory.append({"role": "assistant", "content": response})

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