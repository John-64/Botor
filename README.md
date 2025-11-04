# Botor
This repository contains my university project for thesis.

<p align="center"> 
    <img src="media/BotorMascotte.png" alt="Botor" width="250" height="250">
</p>

## Requirements
- Install [Python](https://www.python.org/);
- Install [Docker](https://www.docker.com/products/docker-desktop/).

## Instruction
1. Launch the Docker application and run this two command:
   - docker pull qdrant/qdrant
3. Download the project and extract it
5. Edit the config.json with at least your API key
6. Open the terminal and go to the located project folder
7. Then run this two commands: 
  - To create and load the Vector Database with your files: python ingest.py (this operation require some minutes)
  - To run the Database: docker run -p 6333:6333 qdrant/qdrant
8. Now you can run this command and start to use Botor:
  - python botor.py

If everything is ok you can use the Botor app by reaching the address shown in the Port(s) section (for example http://localhost:9000).

## Demo 📷
![gif](media/Botor.gif)

### Curiosity
The name "Botor" is a combination of "Bot" with the "Doctor".

#### Credits
- [OpenAI](https://openai.com/)
- [Qdrant](https://qdrant.tech/)
- [Dataset](https://github.com/abachaa/MedQuAD)
