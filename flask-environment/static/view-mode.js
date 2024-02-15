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
    } else if (body.classList == "light-mode") {
        document.getElementById('dark-mode').style.display = 'block';
        document.getElementById('light-mode').style.display = 'none';

        document.getElementById('chatbot').classList.remove('dark-mode');
        document.getElementById('chatbot').classList.add('light-mode');
        document.getElementById('userInput').classList.remove('dark-mode');
        document.getElementById('userInput').classList.add('light-mode');
    }
}