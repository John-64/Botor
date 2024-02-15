# Botor 🩺
This repository contains my university project for the external internship. The application, written in Python, consists of a chatbot capable of answering a human question using FHIR resources taken from a [HAPI FHIR Test Server](https://hapi.fhir.org/).

## Requirements 📝
- Install [Docker](https://www.docker.com/products/docker-desktop/);
- Download the LLM in gguf format [here](https://huggingface.co/TheBloke) (check that it is compatible with Llama, i recommend [this](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) one).

## Instruction 📖
1. Launch the Docker application
2. Download the project and extract it
3. Place model.gguf in the "model" folder, inside the Botor project
4. Edit the config.json with your API key and the name of your LLM.gguf
5. Open terminal and go to the located project folder
6. Then run this two commands: 
  - docker build -t botor .
  - docker run --ulimit memlock=-1:-1 -it -p 9000:5000 --name botor -d botor

You can now verify successful installation by going to the Docker desktop app and checking the images and container. If everything is ok, the container will have the "Running" status and we will be able to use the Botor app by reaching the address shown in the Port(s) section (for example http://localhost:9000).

### Usefull commands 🛠️
- Run this command if you want to know what are the images avaible: docker images
- Run this command to see the stats (like cpu/ram used) of your container: docker stats botor

## Demo 🎥
![gif](./model/Botor.gif)

Here are the operations performed:
- Provide me the information of patient 30163
- Provide me the observation of patient 30163 with code 8310-5 "Body temperature"
- Provide me the observation of patient 30163 with code 3141-9 "Body weight Measured"

### Curiosity 🧐
The name "Botor" is the merge of "Bot" with the "Doctor".
