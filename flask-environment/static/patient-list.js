var json_patients;
var counterLoad = 0;


document.addEventListener('DOMContentLoaded', function () {
    loadPatientList().then(success => {
        if (success) {
            if (counterLoad < 1) {
                printPatientList();
                counterLoad++;
            }
        } else {
            console.error('La richiesta per i pazienti ha fallito.');
        }
    });
    
    document.getElementById('patients-tab').addEventListener('click', function () {
        document.getElementById('patients-tab').className = "active";
        document.getElementById('chat-button').className = "";
        document.getElementById('patients-modal').style.display = 'block';
    });
    
    document.querySelector('.close').addEventListener('click', function () {
        document.getElementById('patients-tab').className = "";
        document.getElementById('chat-button').className = "active";
        document.getElementById('patients-modal').style.display = 'none';
    }); 
});


function loadPatientList() {
    const fhirEndpoint = 'https://hapi.fhir.org/baseR4/Patient';

    return fetch(fhirEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Errore HTTP! Status: ${response.status}`);
            }

            return response.json();
        })
        .then(data => {
            json_patients = data;
            // Ora 'data' contiene il JSON, puoi fare quello che vuoi con esso
            console.log(data);
            return true; // Restituisci true se tutto è andato bene
        })
        .catch(error => {
            console.error('Errore durante la richiesta:', error);
            return false; // Restituisci false in caso di errore
        });
}


function printPatientList() {
    const patientList = document.getElementById('patient-list');

    if (!patientList) {
        console.error('Container della lista pazienti non trovato.');
        return;
    }

    // Verifica se la variabile 'json_patients' è definita
    if (typeof json_patients === 'undefined' || json_patients.entry === undefined) {
        console.error('Dati dei pazienti non trovati o nel formato errato.');
        return;
    }

    const patients = json_patients.entry;

    patients.forEach(paziente => {
        const patientId = paziente?.resource?.id;
        const patientName = paziente?.resource?.name?.[0]?.given?.[0] || 'Not';
        const patientFamilyName = paziente?.resource?.name?.[0]?.family || 'avaible.';

        const fullName = patientName + " " + patientFamilyName;

        const listItem = document.createElement('li');
        listItem.textContent = `• ${patientId}: ${fullName}`;
        patientList.appendChild(listItem);
    });
}
