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
    if (event.keyCode === 13) {
        event.preventDefault();
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
            botText.innerHTML = response.result; 
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


function uploadFile() {
    var formData = new FormData();
    var file = $('#file-upload')[0].files[0];
    formData.append('file', file);

    $.ajax({
        url: '/upload', 
        type: 'POST',
        data: formData,
        processData: false, 
        contentType: false, 
        success: function(response) {
            console.log(response); 
            $('#file-text').text(file.name); 
            $('#file-text').attr("title", file.name);
            $('#file-text').show(); 
            $('#remove-file').show(); 
            $('#file-icon-upload').show(); 
            $('#file-upload-label').hide(); 
            $('#menu-patient').hide(); 
        },
        error: function(error) {
            console.error(error); 
        }
    });
}


$('#file-upload').on('change', function() {
    uploadFile();
});


$('#remove-file').on('click', function() {
    $('#file-upload').val(''); 
    $('#file-text').hide(); 
    $('#remove-file').hide(); 
    $('#file-icon-upload').hide();
    $('#file-upload-label').show(); 
    $('#menu-patient').show();
});


function deleteFiles() {
    $.ajax({
        url: '/delete-files', 
        type: 'POST',
        success: function(response) {
            console.log(response); 
            $('#file-text').hide(); 
            $('#remove-file').hide(); 
            $('#file-upload-label').show(); 
        },
        error: function(error) {
            console.error(error); 
        }
    });
}


$('#remove-file').on('click', function() {
    deleteFiles(); 
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('info-tab').addEventListener('click', function () {
        document.getElementById('info-modal').style.display = 'block';
    });
    
    document.querySelector('.close').addEventListener('click', function () {
        document.getElementById('info-modal').style.display = 'none';
    }); 
});


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