var userInput = document.getElementById("userInput");
userInput.value = "";

function testJSON(text) {
    if (typeof text !== "string") {
        return false;
    }
    try {
        JSON.parse(text);
        return true;
    } catch (error) {
        return false;
    }
}

function handleKeyPress(event) {
    // Verifica se il tasto premuto è "Invio" (codice 13)
    if (event.keyCode === 13) {
        // Impedisce il comportamento predefinito (ad es. il submit del modulo)
        event.preventDefault();
        // Chiama la funzione sendMessage()
        sendMessage();
    }
}

function sendMessage() {
    if(document.getElementById('userInput').value != "") {
        generateResponse();
    }
}

function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
    }
    return result;
}

    
function generateResponse() {
    var button = document.getElementById('button-send');
    button.disabled = true;

    var input = document.getElementById('userInput').value;
    document.getElementById('userInput').value = "";

    var chatBox = document.getElementById("chatBox");
    var userMessage = document.createElement("div");
    var userText = document.createElement("span");
    userText.innerHTML = input;
    userMessage.className = "question-side";
    userText.className = "question-text";
    userMessage.appendChild(userText);
    chatBox.appendChild(userMessage);
    chatBox = document.getElementById("chatBox");

    chatBox.scrollTop = chatBox.scrollHeight;
    chatBox.style.overflowY = "auto"

    var botMessage = document.createElement("div");
    var botText = document.createElement("span");
    var loadingContainer = document.createElement("div");
    var loading = document.createElement("div");
    var spinner = document.createElement("div");

    setTimeout(function() {
        loadingContainer.className = "loading-container";
        loading.className = "loading";
        loading.innerHTML = "O";
        spinner.className = "spinner";
        loadingContainer.appendChild(loading);
        loading.appendChild(spinner);

        botMessage.className = "answer-side";
        botText.className = "answer-text";

        botMessage.appendChild(loadingContainer);
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
        chatBox.style.overflowY = "auto"
    }, 500);

    $.ajax({ 
        url: '/process', 
        type: 'POST', 
        contentType: 'application/json', 
        data: JSON.stringify({ 'value': input }), 
        success: function(response) {
            button.disabled = false;
            botText.innerHTML = response.result; // Utilizza response.result anziché response
            botMessage.removeChild(loadingContainer);
            botMessage.appendChild(botText);
            chatBox.scrollTop = chatBox.scrollHeight;
            chatBox.style.overflowY = "auto";
        }, 
        error: function(error) {
            console.log(error); 
        } 
    });
}

// Funzione per gestire l'invio del file
function uploadFile() {
    var formData = new FormData();
    var file = $('#file-upload')[0].files[0];
    formData.append('file', file);

    $.ajax({
        url: '/upload', // L'URL al quale inviare la richiesta POST
        type: 'POST',
        data: formData,
        processData: false, // Non elaborare i dati
        contentType: false, // Non impostare l'intestazione Content-Type
        success: function(response) {
            console.log(response); // Gestisci la risposta dal server
            $('#file-text').text(file.name); // Mostra il nome del file caricato
            $('#file-text').attr("title", file.name);
            $('#file-text').show(); // Mostra l'icona del nome del file
            $('#remove-file').show(); // Mostra l'icona di rimozione del file
            $('#file-icon-upload').show(); // Mostra l'icona di rimozione del file
            $('#file-upload-label').hide(); // Nascondi il pulsante di caricamento
            $('#menu-patient').hide(); // Nascondi il pulsante di caricamento
        },
        error: function(error) {
            console.error(error); // Gestisci eventuali errori
        }
    });
}

// Aggiungi un ascoltatore di eventi per l'input file
$('#file-upload').on('change', function() {
    uploadFile();
});

// Aggiungi un ascoltatore di eventi per l'icona di rimozione del file
$('#remove-file').on('click', function() {
    $('#file-upload').val(''); // Rimuovi il file selezionato
    $('#file-text').hide(); // Nascondi l'icona del tipo di file
    $('#remove-file').hide(); // Nascondi l'icona di rimozione del file
    $('#file-icon-upload').hide();
    $('#file-upload-label').show(); // Mostra il pulsante di caricamento
    $('#menu-patient').show();
});

// Funzione per eliminare i file
function deleteFiles() {
    $.ajax({
        url: '/delete-files', // L'URL al quale inviare la richiesta POST per eliminare i file
        type: 'POST',
        success: function(response) {
            console.log(response); // Gestisci la risposta dal server
            $('#file-text').hide(); // Nascondi l'icona del nome del file
            $('#remove-file').hide(); // Nascondi l'icona di rimozione del file
            $('#file-upload-label').show(); // Mostra il pulsante di caricamento
        },
        error: function(error) {
            console.error(error); // Gestisci eventuali errori
        }
    });
}

// Aggiungi un ascoltatore di eventi per l'icona di rimozione del file
$('#remove-file').on('click', function() {
    deleteFiles(); // Chiamare la funzione deleteFiles quando si fa clic sulla X
});

/*
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('info-tab').addEventListener('click', function () {
        button = document.getElementById('info-tab').className = "active";
        document.getElementById('info-modal').style.display = 'block';
    });
    
    document.querySelector('.close').addEventListener('click', function () {
        document.getElementById('info-tab').className = "";
        document.getElementById('info-modal').style.display = 'none';
    }); 
});

<div id="chatBox">
    <div class="answer-side">
        <span class="answer-text">Hi! My name is Botor and i will answer to all your question.</span>
    </div>
</div>
*/

// Funzione per gestire il clic su un paziente
function selectPatient(patient) {
    var selectedIconElement = patient.querySelector('.patient-selected-icon');
    selectedIconElement.style.setProperty('display', 'block', 'important');
    
    var initials = patient.dataset.value.split('').filter(char => char.toUpperCase() === char && char !== ' ').join('');

    var chatBox = document.getElementById('chatBox');

    var botMessage = document.createElement('div');
    botMessage.classList.add('answer-side');
    var botText = document.createElement('span');
    botText.classList.add('answer-text');
    botText.textContent = "Ask me something about " + patient.dataset.value + "!";
    botMessage.appendChild(botText);
    chatBox.appendChild(botMessage);
    chatBox.scrollTop = chatBox.scrollHeight;
    chatBox.style.overflowY = "auto";

    $('.list-patient').hide();
    $('.initial-name').text(initials);
    $('.initial-name').show();
    $('#upload').hide();

    $.ajax({
        url: '/selected_patient',
        type: 'POST',
        data: { patient_name: patient.dataset.value },
        success: function(response) {
            console.log('Paziente selezionato correttamente.');
        },
        error: function(error) {
            console.error('Errore durante l\'invio della selezione:', error);
        }
    });
}

function clearAllX() {
    var allPatients = document.querySelectorAll('.menu-content .patient');
    allPatients.forEach(patient => {
        var selectedIconElement = patient.querySelector('.patient-selected-icon');
        selectedIconElement.style.display = 'none';
    });
    $('.initial-name').hide();
}

var patients = document.querySelectorAll('#menu-patient .menu-content .patient');
    patients.forEach(patient => {
        patient.addEventListener('click', function() {
            clearAllX();
            selectPatient(this);
    });
});

var closes = document.querySelectorAll('.menu-content .patient .patient-selected-icon');
closes.forEach(closeIcon => {
    closeIcon.addEventListener('click', function(event) {
        event.stopPropagation();
        
        $.ajax({
            url: '/selected_patient',
            type: 'POST',
            data: { patient_name: "None"},
            success: function(response) {
                console.log('Paziente selezionato correttamente.');
            },
            error: function(error) {
                console.error('Errore durante l\'invio della selezione:', error);
            }
        });

        closeIcon.style.display = 'none';

        var chatBox = document.getElementById('chatBox');

        var botMessage = document.createElement('div');
        botMessage.classList.add('answer-side');
        var botText = document.createElement('span');
        botText.classList.add('answer-text');
        botText.textContent = "User removed.";
        clearAllX();
        botMessage.appendChild(botText);
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
        chatBox.style.overflowY = "auto";

        $('.initial-name').text("");
        $('.initial-name').hide();
        $('.list-patient').show();
        $('#upload').show();
    });
});

