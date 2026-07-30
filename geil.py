import streamlit as st
import base64
import os
import time
import google.genai as genai
from google.genai import types
import google.genai.errors

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin KI-ASSISTENT")

# HIER DEINE EIGENEN GOOGLE GEMINI SCHLÜSSEL EINTRAGEN:
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

# Das unblockierbare Empfänger-Feld nimmt den Text von JavaScript entgegen
sprach_input = st.text_input("Schnittstelle", key="hidden_voice_input", label_visibility="collapsed")

if sprach_input:
    st.session_state.ki_antwort = frage_ki(sprach_input)

# CSS zum kompletten Verstecken des Textfeldes im Hintergrund
st.markdown("""
    <style>
    div[data-testid="stTextInput"] {
        position: absolute !important;
        top: -1000px !important;
        left: -1000px !important;
        opacity: 0 !important;
        height: 0px !important;
        width: 0px !important;
        overflow: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)
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
        // PERFEKTER UND AUSFÜHRLICHER BROWSER-INDEX-PFAD
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
            
            // Unblockierbarer Input-Weg: Schreibt den Text virtuell in das unsichtbare Python-Textfeld
            const inputs = window.parent.document.getElementsByTagName('input');
            if (inputs.length > 0) {
                const targetInput = inputs[0];
                targetInput.value = gehoert;
                
                targetInput.dispatchEvent(new Event('input', { bubbles: true }));
                targetInput.dispatchEvent(new Event('change', { bubbles: true }));
                
                setTimeout(() => {
                    const form = targetInput.form;
                    if (form) {
                        form.requestSubmit();
                    } else {
                        const ke = new KeyboardEvent('keydown', { bubbles: true, cancelable: true, keyCode: 13, key: 'Enter' });
                        targetInput.dispatchEvent(ke);
                    }
                }, 50);
            }
        }
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Ersetzt alle Musik-Platzhalter absolut crashsicher direkt in Python
html_bereit = html_reine_web_app.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)

# Haupt-App im iFrame anzeigen (Ohne key= Argument, um Python 3.14 Abstürze zu verhindern)
st.components.v1.html(html_bereit, height=270)

# Wenn Python die Antwort berechnet hat, schleusen wir sie direkt zur Vorlese-Ausgabe ein
if st.session_state.ki_antwort:
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
