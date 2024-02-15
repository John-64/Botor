import flask
import requests
import json
from openai import OpenAI
from llama_cpp import Llama

app = flask.Flask(__name__, template_folder='./flask-environment/templates', static_folder='./flask-environment/static')

# Extracting the settings from config.json
with open("./config.json", "r") as c:
    config = json.load(c)

    API_KEY = config["api_key"]

    model_path = config["model_path"]
    temperature = float(config["temperature"])
    max_tokens = int(config["max_tokens"])
    n_ctx = int(config["n_ctx"])
    top_p = int(config["top_p"])

# Defining a function for extract the main information from a question made in natural language and return a FHIR query
def generate_query(question):
    # Check out all the models here: https://platform.openai.com/docs/models/overview
    GPT_MODEL = "gpt-3.5-turbo-1106"

    # Setting up the client
    client = OpenAI(api_key = API_KEY)

    # Prompt for OpenAI
    messages = [
        {"role": "system", "content": "Follow this form for build the query: 'https://hapi.fhir.org/baseR4/replace-with-information'. Please, study it!"
        },
        {"role": "user", "content": question},
        {"role": "system", "content": 'Generate a query without additional information, format or ordering. Provide only the requested query, and refrain from adding any other details, explanations, or personal opinions. Follow the request strictly. Replace the information you want to add with "replace-with-information". If you are unable to follow these instructions, return "It is not possible to fulfill your request. Please try again with a more specific question." '
        },
        {"role": "system", "content": 'If the user want more than 1 operation per time, return "Please, search for one piece of information at a time."'
        },
    ]

    # Get the answer
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        max_tokens=100,
        temperature=0
    )

    # Extract the answer
    query = response.choices[0].message.content
    return query

# Defining a function for understand if is possible to print the chart or the text
def check_json_fields(json_data):
    try:
        # Parsing the JSON
        data = json.loads(json_data)

        # Check if "entry" is in the JSON
        if 'entry' in data:
            for entry in data['entry']:
                if 'resource' in entry and 'effectiveDateTime' in entry['resource'] and 'valueQuantity' in entry['resource']:
                    return True
            # If not
            return False
        else:
            # If yes
            return False

    except json.JSONDecodeError as e:
        print(f"Error during the JSON parsing: {e}")
        return False

@app.route('/process', methods=['POST']) 
def process():  
    # Taking the question from the user
    data = flask.request.get_json()
    question = data['value']

    query = generate_query(question)

    # Check if the user have asked something different from the chatbot operating field
    if query != "It is not possible to fulfill your request. Please try again with a more specific question." and query !="Please, search for one piece of information at a time.":
        # Server resource fetching
        json_answer = requests.get(query)

        if check_json_fields(json_answer.text):
            data = json_answer.json()
            array = []

            # Iterate through observations in the JSON
            for entry in data.get('entry', []):
                info_data = entry.get('resource', {})

                # Extract the desired values ​​for each observation
                id = info_data.get('id', '')
                status = info_data.get('status', '')
                code_text = info_data.get('code', {}).get('text', '')
                effective_date_time = info_data.get('effectiveDateTime', '')
                value = info_data.get('valueQuantity', {}).get('value', '')
                unit = info_data.get('valueQuantity', {}).get('unit', '')

                # Add to the array
                value = [id, status, code_text, effective_date_time, value, unit]
                array.append(value)

            return flask.jsonify(result="none", graph=array)
        else:
            llm = Llama(
                model_path=model_path,
                temperature=temperature,
                max_tokens=max_tokens,
                n_ctx=n_ctx,
                top_p=top_p
            )
            
            # Variable containing the textual JSON for greater readability
            json_text = json_answer.text

            # Prompt for LLM including the JSON requested
            prompt = f"""
            [INST]<<SYS>>
            You are a helpful, respectful and honest medical assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

            Given the following patient information JSON, create a human-readable sentence describing the patient:

            {json_text}

            Create a sentence that includes the patient's information.
            [/INST]
            """
            # Generating the answer
            output = llm(prompt = prompt, max_tokens = 250, temperature = 0.5)
             # Variable containing the response for greater readability
            result = output['choices'][0]['text']

            return flask.jsonify(result=result, graph="none")
    else:
        return flask.jsonify(result=query, graph="none")
    
@app.route('/')
def home():
    return flask.render_template('home.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True, debug=True)