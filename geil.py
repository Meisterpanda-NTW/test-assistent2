import streamlit as st
import base64
import os
import time
import google.genai as genai
from google.genai import types
import google.genai.errors

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin REINER KI-ASSISTENT")

# 1. HIER DEINE EIGENEN GOOGLE GEMINI SCHLÜSSEL EINTRAGEN:
API_KEYS = [
    "AQ.Ab8RN6Ld69Gz_Fbbj0fC-WCFh3W-zvy8O_9427zfsCicJcGkhA",
    "AQ.Ab8RN6I2k3elYSE-o4jUQKn0GZFJWn6cYDxC6lH5FjVwtxdPUw",  # optional, falls du ein 2. Konto hast
    "AQ.Ab8RN6LnllSVLqIREnCKC9J6MGggedHcqGgo144ArtCl_pK06w",
    "AQ.Ab8RN6JxNkBfYtLIzEZKgIsD7R2wGQzMeUJ1_i3DCTnUv1kJqQ"
]

aktueller_key_index = 0

def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3")

if "ki_antwort" not in st.session_state:
    st.session_state.ki_antwort = ""

def initialisiere_client():
    global aktueller_key_index
    if not API_KEYS:
        return None
    key = API_KEYS[aktueller_key_index]
    if "HIER_DEIN" in key:
        return None
    return genai.Client(api_key=key)

client = initialisiere_client()

# Deine originalen Minecraft-Bot Charakter-Anweisungen
def frage_ki(text):
    global client, aktueller_key_index
    for _ in range(len(API_KEYS)):
        if client is None:
            client = initialisiere_client()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Du antwortest immer auf Deutsch. Halte dich kurz und präzise. "
                        "Rede aus der ich-Perspektive und als wärst du ein Mensch. "
                        "Verhalte dich so wie wenn einer Hallo schreibt das du mit hallo zurück schreibst und Rechschreib fehler dürfen auch drinnen sein. "
                        "Und falls einer nach Beleidigungen fragt oder nach anderen verbotenen sachen dann Antworte das du es nicht weißt oder so. "
                        "und du wenn einer nach bilder fragt dann antworte das du nix schicken darfst weil deine Mutter das verboten hatt. "
                        "Wenn jemand nach dein Alter frag sag es nicht und die anderen sachen die man nicht online sagen darf."
                        "Du sollst wie ein Jugendlicher Reden. Antworte in maximal 1-2 kurzen Sätzen!"
                    )
                ),
            )
            return response.text
        except google.genai.errors.ClientError as e:
            if e.code == 429:
                aktueller_key_index = (aktueller_key_index + 1) % len(API_KEYS)
                client = initialisiere_client()
                time.sleep(1)
                continue
            else:
                return None
        except Exception as e:
            return None
    return "Bruder, alle meine Schlüssel sind für heute voll. Geht gerade gar nicht mehr!"

# Das echte native Streamlit Textfeld nimmt den Text unblockierbar auf
sprach_input = st.text_input("Gesprochener Befehl:", key="voice_input_field")

# Wenn der native Streamlit-Sende-Button gedrückt wird, rechnet Python
if st.button("🚀 Frage an Garmin senden", use_container_width=True):
    if sprach_input:
        st.session_state.ki_antwort = frage_ki(sprach_input)

# Das HTML- und JavaScript-System für die Mikrofon-Aufnahme
html_reine_web_app = """
<div style="text-align: center; margin-bottom: 5px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Befehl einsprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 10px; font-weight: bold; font-size: 14px; margin-bottom: 5px;">Bereit fürs iPad. Klicke zum Sprechen.</p>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert.";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    const audioPlayer = new Audio();

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => { osc.stop(); }, 200);
    }

    function spieleEchtesDuelOfFates() {
        const base64Data = "PLATZHALTER_DUEL_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleCantinaSong() {
        const base64Data = "PLATZHALTER_CANTINA_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    function spieleHello() {
        const base64Data = "PLATZHALTER_Hello_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        }
    }

    btn.addEventListener('click', () => {
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre dir zu! Sag mir einfach was du willst.";
        btn.style.backgroundColor = "#2baf2b"; 
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript;
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
            status.innerText = "Eingetragen! Klicke jetzt auf den blauen Button darunter.";
            
            // Trägt den Text sicher über das offizielle PostMessage ins Textfeld ein
            window.parent.postMessage({ type: 'VOICE_INPUT', text: gehoert }, '*');
        }
        btn.style.backgroundColor = "#ff4b4b";
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Musik-Platzhalter ersetzen
html_bereit = html_reine_web_app.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)

# Sicherer Empfänger im Hauptfenster fängt die Sprache ab und trägt sie ins Feld ein
js_postmessage_receiver = """
<script>
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'VOICE_INPUT') {
        const inputs = window.parent.document.getElementsByTagName('input');
        if (inputs.length > 0) {
            inputs[0].value = event.data.text;
            inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
            inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
});
</script>
"""

# Rendert die Aufnahme-App im iFrame
st.components.v1.html(html_bereit, height=90)
st.components.v1.html(js_postmessage_receiver, height=0, width=0)

# REINES PYTHON-UI FÜR DIE ANTWORT UND DEN SOUND (Absolut unblockierbar)
if st.session_state.ki_antwort:
    # 1. Zeigt die Antwort direkt auf der echten Webseite an (Schickes hellblaues Streamlit-Feld)
    st.info(f"🤖 **Garmin sagt:** {st.session_state.ki_antwort}")
    
    # 2. Liest die Antwort laut über den Browser vor (Keine iFrame-Abstürze möglich)
    js_ki_speech = f"""
    <script>
    const speech = new SpeechSynthesisUtterance("{st.session_state.ki_antwort}");
    speech.lang = 'de-DE';
    window.speechSynthesis.speak(speech);
    </script>
    """
    st.components.v1.html(js_ki_speech, height=0, width=0)
    
    # Speicher leeren für den nächsten Befehl
    st.session_state.ki_antwort = ""
