import streamlit as st
import base64
import os
import json

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin REINER KI-ASSISTENT")

# 1. HIER DEINE EIGENEN GOOGLE GEMINI SCHLÜSSEL EINTRAGEN:
API_KEYS = [
    "AQ.Ab8RN6Ld69Gz_Fbbj0fC-WCFh3W-zvy8O_9427zfsCicJcGkhA",
    "AQ.Ab8RN6I2k3elYSE-o4jUQKn0GZFJWn6cYDxC6lH5FjVwtxdPUw",  # optional, falls du ein 2. Konto hast
    "AQ.Ab8RN6LnllSVLqIREnCKC9J6MGggedHcqGgo144ArtCl_pK06w",
    "AQ.Ab8RN6JxNkBfYtLIzEZKgIsD7R2wGQzMeUJ1_i3DCTnUv1kJqQ"
]


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

# Das komplette HTML- und JavaScript-System für den Browser (Teil 2 von 2)
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
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript;
        const gehoertLower = gehoert.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        machPiep();

        if (gehoertLower.includes("duel of fates") || gehoertLower.includes("schicksal")) {
            spieleEchtesDuelOfFates();
            btn.style.backgroundColor = "#ff4b4b";
        } else if (gehoertLower.includes("cantina") || gehoertLower.includes("bar")) {
            spieleCantinaSong();
            btn.style.backgroundColor = "#ff4b4b";
        } else if (gehoertLower.includes("hello")) {
            spieleHello();
            btn.style.backgroundColor = "#ff4b4b";
        } else if (gehoertLower.includes("beenden") || gehoertLower.includes("stopp")) {
            audioPlayer.pause();
            rec.stop();
            btn.style.backgroundColor = "#ff4b4b";
        } else if (gehoertLower.length > 0) {
            status.innerText = "🤖 Garmin überlegt...";
            
            // UNBLOCKIERBARER TUNNEL: Schreibt den Text in den iFrame-Hash. Das überwindet alle CORS-Sperren!
            window.location.hash = "voice=" + encodeURIComponent(gehoert);
        }
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Wenn der iFrame-Hash von Python ausgelesen wird, verarbeiten wir den Text im sicheren Server-Umfeld
import urllib.parse
html_final = html_reine_web_app

# JavaScript injizieren, um den Hash nach der Verarbeitung wieder sauber zu leeren
js_hash_cleaner = ""

if "ki_antwort" in st.session_state and st.session_state.ki_antwort:
    st.success(st.session_state.ki_antwort)
    
    js_ki_speech_template = """
    <script>
    window.parent.document.getElementById('antwort-box').innerText = "TAUSCH_TEXT";
    window.parent.document.getElementById('antwort-box').style.backgroundColor = "#d1ecf1";
    window.parent.document.getElementById('antwort-box').style.color = "#0c5460";
    window.parent.document.getElementById('antwort-box').style.display = "block";
    
    const speech = new SpeechSynthesisUtterance("TAUSCH_TEXT");
    speech.lang = 'de-DE';
    window.speechSynthesis.speak(speech);
    </script>
    """
    js_ki_speech_bereit = js_ki_speech_template.replace("TAUSCH_TEXT", st.session_state.ki_antwort)
    st.components.v1.html(js_ki_speech_bereit, height=0, width=0)
    st.session_state.ki_antwort = ""
    js_hash_cleaner = "<script>window.location.hash = '';</script>"

# Musik-Streams ersetzen
html_bereit = html_final.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)
html_ausgabe = html_bereit + js_hash_cleaner

# Rendert das Hauptfenster flüssig und ohne iFrame-SDK-Abstürze
st.components.v1.html(html_ausgabe, height=270)
