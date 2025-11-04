# Botor
This repository contains my university thesis project.

<p align="center"> 
    <img src="media/BotorMascotte.png" alt="Botor" width="250" height="250">
</p>

## Requirements
- Install [Python](https://www.python.org/);
- Install [Docker](https://www.docker.com/products/docker-desktop/).

## Instruction
1. Start Docker, then run the following command to download Qdrant:
    ```bash
    docker pull qdrant/qdrant
2. Download the project and extract it.
3. Edit the config.json file — at minimum, add your API key.
4. Open a terminal and navigate to the project folder.
5. Run the following commands:
  - To create and load the Vector Database with your files (this process may take a few minutes):
    ```bash
    python ingest.py 
  - To run the Database:
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
6. Start Botor:
    ```bash
    python botor.py
    ```
7. If everything is configured correctly, you can use Botor by opening the address displayed in the Port(s) section, for example:
     ```bash
     http://localhost:90005

## Demo 📷
<p align="center" width="40%">
  <img src="media/Botor.gif" alt="Botor" width="80%">
</p>

#### Credits
- [OpenAI](https://openai.com/)
- [Qdrant](https://qdrant.tech/)
- [Dataset](https://github.com/abachaa/MedQuAD)

### Curiosity
The name "Botor" is a combination of "Bot" with the "Doctor".

## Info
This project was created for the course "Sicurezza dei Dati" at the Università degli Studi di Salerno.

## Contribution
If you'd like to contribute to Bloky, please follow these steps:
- Fork the repository.
- Create a new branch (git checkout -b feature/YourFeatureName).
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/YourFeatureName).
- Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
