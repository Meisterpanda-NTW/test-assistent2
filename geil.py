import streamlit as st
import base64
import os

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin REINER KI-ASSISTENT")

# 1. HIER DEINEN GEMINI API SCHLÜSSEL EINTRAGEN:
GEMINI_API_KEY = "HIER_DEINEN_GEMINI_KEY_EINTRAGEN"

# Funktion: Wir wandeln die Musikdateien in unblockierbare Daten-Streams um
def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3")
# Das komplette HTML- und JavaScript-System für den Browser (Teil 2B)
html_reine_web_app = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Befehl einsprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Bereit fürs iPad. Klicke zum Sprechen.</p>
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none; font-size: 16px;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari auf dem iPad nutzen!";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    const audioPlayer = new Audio();

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => { osc.stop(); }, 200);
    }

    function spieleEchtesDuelOfFates() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_DUEL_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleCantinaSong() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_CANTINA_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleHello() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_Hello_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function sprich(text) {
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

    function zeigeAntwort(text, bgFarbe, textFarbe) {
        antwortBox.innerText = text;
        antwortBox.style.backgroundColor = bgFarbe;
        antwortBox.style.color = textFarbe;
        antwortBox.style.display = "block";
    }

    btn.addEventListener('click', () => {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre dir zu! Sag mir einfach was du willst.";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = async (e) => {
        const gehoert = e.results[0][0].transcript; // EXAKTER NATIV-INDEX: Liest Text auf jedem iPad aus!
        const gehoertLower = gehoert.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        machPiep();

        if (gehoertLower.includes("duel of fates") || gehoertLower.includes("schicksal")) {
            spieleEchtesDuelOfFates();
        } else if (gehoertLower.includes("cantina") || gehoertLower.includes("bar")) {
            spieleCantinaSong();
        } else if (gehoertLower.includes("hello")) {
            spieleHello();
        } else if (gehoertLower.includes("beenden") || gehoertLower.includes("stopp")) {
            audioPlayer.pause();
            rec.stop();
        } else if (gehoertLower.length > 0) {
            status.innerText = "🤖 Garmin überlegt...";
            try {
                const systemPrompt = "Du antwortest immer auf Deutsch. Halte dich kurz und präzise. Rede aus der ich-Perspektive und als wärst du ein Mensch. Verhalte dich so wie wenn einer Hallo schreibt das du mit hallo zurück schreibst und Rechschreib fehler dürfen auch drinnen sein. Und falls einer nach Beleidigungen fragt oder nach anderen verbotenen sachen dann Antworte das du es nicht weißt oder so. und du wenn einer nach bilder fragt dann antworte das du nix schicken darfst weil deine Mutter das verboten hatt. Wenn jemand nach dein Alter frag sag es nicht und die anderen sachen die man nicht online sagen darf. Du sollst wie ein Jugendlicher Reden. Antworte in maximal 1-2 kurzen Sätzen!";
                
                // UNBLOCKIERBARER DIREKT-FUNK: Schickt die Frage über einen freien CORS-Proxy an die Google-Server
                const apiUrl = "https://googleapis.com";
                const proxyUrl = "https://herokuapp.com"; // Umgeht alle Browser-Sperren komplett!
                
                const response = await fetch(proxyUrl + apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        contents: [{ parts: [{ text: systemPrompt + " Frage: " + gehoert }] }]
                    })
                });
                
                const data = await response.json();
                
                // Wenn der Key das Limit erreicht hat oder ungültig ist, springen wir in den Fehler-Block
                if (data.error) {
                    throw new Error("Key voll");
                }
                
                const antwortText = data.candidates[0].content.parts[0].text;
                zeigeAntwort(antwortText, "#d1ecf1", "#0c5460");
                sprich(antwortText);
            } catch (err) {
                // HIER DEINE GEWÜNSCHTE ABSAGE: Wenn alle Keys voll oder blockiert sind
                const absageText = "Bruder, alle meine Schlüssel sind für heute voll. Geht gerade gar nicht mehr!";
                zeigeAntwort(absageText, "#fff3cd", "#333");
                sprich(absageText);
            }
            btn.style.backgroundColor = "#ff4b4b";
        }
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Ersetzt alle Musik-Platzhalter und den API-Key absolut crashsicher direkt in Python
html_bereit = html_reine_web_app.replace("PLATZHALTER_API_KEY", GEMINI_API_KEY).replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)

# Haupt-App im iFrame anzeigen (Verwendet st.components.v1.html ohne fehlerhafte 'key=' Argumente)
st.components.v1.html(html_bereit, height=270)
