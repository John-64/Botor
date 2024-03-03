function checkTheme() {
    const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
    if (!darkThemeMq.matches) {
        toggleMode();
        document.getElementById('dark-mode').style.display = 'block';
        document.getElementById('light-mode').style.display = 'none';
    }
}

function toggleMode() {
    var body = document.body;
    body.classList.toggle("dark-mode");
    body.classList.toggle("light-mode");
    if(body.classList == "dark-mode") {
        document.getElementById('dark-mode').style.display = 'none';
        document.getElementById('light-mode').style.display = 'block';

        document.getElementById('chatbot').classList.add('dark-mode');
        document.getElementById('chatbot').classList.remove('light-mode');
        document.getElementById('userInput').classList.add('dark-mode');
        document.getElementById('userInput').classList.remove('light-mode');
        document.getElementById('modal-id').classList.add('dark-mode');
        document.getElementById('modal-id').classList.remove('light-mode');
        document.getElementById('change-mode').classList.add('dark-mode');
        document.getElementById('change-mode').classList.remove('light-mode');
        document.getElementById('title').classList.add('dark-mode');
        document.getElementById('title').classList.remove('light-mode');
        document.getElementById('input-container').classList.add('dark-mode');
        document.getElementById('input-container').classList.remove('light-mode');
        document.getElementById('button-send').classList.add('dark-mode');
        document.getElementById('button-send').classList.remove('light-mode');
        document.getElementById('upload').classList.add('dark-mode');
        document.getElementById('upload').classList.remove('light-mode');
        document.getElementById('file-upload-label').classList.add('dark-mode');
        document.getElementById('file-upload-label').classList.remove('light-mode');
        document.getElementById('file-icon-upload').classList.add('dark-mode');
        document.getElementById('file-icon-upload').classList.remove('light-mode');
        document.getElementById('file-text').classList.add('dark-mode');
        document.getElementById('file-text').classList.remove('light-mode');
        document.getElementById('remove-file').classList.add('dark-mode');
        document.getElementById('remove-file').classList.remove('light-mode');
        document.getElementById('menu-patient').classList.add('dark-mode');
        document.getElementById('menu-patient').classList.remove('light-mode');
    } else if (body.classList == "light-mode") {
        document.getElementById('dark-mode').style.display = 'block';
        document.getElementById('light-mode').style.display = 'none';

        document.getElementById('chatbot').classList.remove('dark-mode');
        document.getElementById('chatbot').classList.add('light-mode');
        document.getElementById('userInput').classList.remove('dark-mode');
        document.getElementById('userInput').classList.add('light-mode');
        document.getElementById('modal-id').classList.remove('dark-mode');
        document.getElementById('modal-id').classList.add('light-mode');
        document.getElementById('change-mode').classList.remove('dark-mode');
        document.getElementById('change-mode').classList.add('light-mode');
        document.getElementById('title').classList.remove('dark-mode');
        document.getElementById('title').classList.add('light-mode');
        document.getElementById('input-container').classList.remove('dark-mode');
        document.getElementById('input-container').classList.add('light-mode');
        document.getElementById('button-send').classList.remove('dark-mode');
        document.getElementById('button-send').classList.add('light-mode');
        document.getElementById('upload').classList.remove('dark-mode');
        document.getElementById('upload').classList.add('light-mode');
        document.getElementById('file-upload-label').classList.remove('dark-mode');
        document.getElementById('file-upload-label').classList.add('light-mode');
        document.getElementById('file-icon-upload').classList.remove('dark-mode');
        document.getElementById('file-icon-upload').classList.add('light-mode');
        document.getElementById('file-text').classList.remove('dark-mode');
        document.getElementById('file-text').classList.add('light-mode');
        document.getElementById('remove-file').classList.remove('dark-mode');
        document.getElementById('remove-file').classList.add('light-mode');
        document.getElementById('menu-patient').classList.remove('dark-mode');
        document.getElementById('menu-patient').classList.add('light-mode');
    }
}