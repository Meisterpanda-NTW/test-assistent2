import streamlit as st
import base64
import os
import time
import google.genai as genai  # HIER REPARIERT: Lädt genai so, wie der Client es braucht!
from google.genai import types
import google.genai.errors

st.set_page_config(page_title="Garmin KI Assistent", page_icon="🤖")
st.title("🤖 Garmin KOSTENLOSER KI-Assistent")

API_KEYS = [
    "AQ.Ab8RN6Ld69Gz_Fbbj0fC-WCFh3W-zvy8O_9427zfsCicJcGkhA",
    "AQ.Ab8RN6I2k3elYSE-o4jUQKn0GZFJWn6cYDxC6lH5FjVwtxdPUw",  # optional, falls du ein 2. Konto hast
    "AQ.Ab8RN6LnllSVLqIREnCKC9J6MGggedHcqGgo144ArtCl_pK06w",
    "AQ.Ab8RN6JxNkBfYtLIzEZKgIsD7R2wGQzMeUJ1_i3DCTnUv1kJqQ"
]

aktueller_key_index = 0

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

# SITZUNGS-SPEICHER FÜR DIE KI
if "ki_antwort" not in st.session_state:
    st.session_state.ki_antwort = ""

def initialisiere_client():
    global aktueller_key_index
    if not API_KEYS or API_KEYS[0].startswith("HIER_DEIN"):
        return None
    key = API_KEYS[aktueller_key_index]
    return genai.Client(api_key=key)

client = initialisiere_client()

def frage_ki(text):
    global client, aktueller_key_index
    if not API_KEYS or API_KEYS[0].startswith("HIER_DEIN"):
        return "Bitte trage deine Gemini API-Keys oben im Python-Code ein!"
        
    for _ in range(len(API_KEYS)):
        if client is None:
            client = initialisiere_client()
        try:
            # Nutzt das ultraschnelle offizielle Gemini Modell
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
                        "Du sollst wie ein jugendlicher Reden. Antworte in maximal 1-2 sehr kurzen Sätzen!"
                    )
                ),
            )
            return response.text
        except Exception as e:
            # Falls das Limit erreicht ist, rotieren wir zum nächsten Key
            aktueller_key_index = (aktueller_key_index + 1) % len(API_KEYS)
            client = initialisiere_client()
            time.sleep(1)
            continue
            
    return "Alle API-Schlüssel sind für heute voll! Bitte kurz warten."

# Dieser CSS-Code versteckt das Tippfeld absolut unsichtbar im Hintergrund
st.markdown("""
    <style>
    div[data-testid="stTextInput"] {
        position: absolute;
        top: -500px;
        left: -500px;
        opacity: 0;
        height: 0;
        width: 0;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Das versteckte Empfänger-Textfeld
sprach_input = st.text_input("Schnittstelle", key="hidden_voice_input", label_visibility="collapsed")

if sprach_input:
    befehl = sprach_input.lower().strip()
    st.session_state.ki_antwort = frage_ki(sprach_input)

# Das HTML-System für den Browser
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
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari (iPad) oder Chrome (PC) nutzen!";
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

    function spieleStarWars() {
        audioPlayer.pause(); 
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const melodie = [
            {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.6}
        ];
        let startZeit = ctx.currentTime;
        melodie.forEach((note) => {
            const osc = ctx.createOscillator();
            const gainNode = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.value = note.f;
            gainNode.gain.setValueAtTime(0.3, startZeit);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startZeit + note.d);
            osc.connect(gainNode);
            gainNode.connect(ctx.destination);
            osc.start(startZeit);
            osc.stop(startZeit + note.d);
            startZeit += note.d + 0.05;
        });
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
        status.innerText = "🔊 Ich höre zu... Sprich jetzt deinen Befehl!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
        // HIER STARTET TEIL 3: Unzerstörbarer Sitzungs-Speicher für das Aktivierungswort
    // Wir merken uns im lokalen Browser-Speicher, ob Garmin schon einmal aufgeweckt wurde
    if (sessionStorage.getItem("garminAktiviert") === null) {
        sessionStorage.setItem("garminAktiviert", "false");
    }

    btn.addEventListener('click', () => {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        try { rec.start(); } catch(e) {}
        
        // Status-Anzeige passt sich an, je nachdem ob er schon aufgeweckt wurde
        if (sessionStorage.getItem("garminAktiviert") === "true") {
            status.innerText = "🔊 Garmin ist wach! Sprich einfach deinen Befehl!";
        } else {
            status.innerText = "🔊 Ich höre zu... Starte mit 'Okay Garmin'!";
        }
        
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript;
        const gehoertLower = gehoert.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        
        let antwortText = "";
        let boxFarbe = "#e2e2e2";
        let textFarbe = "#333";
        let istMusik = false;

        // PRÜFUNG: Wurde "Okay Garmin" gesagt ODER ist die Flagge bereits dauerhaft AKTIV?
        const istSchonWach = sessionStorage.getItem("garminAktiviert") === "true";
        const hatAufgeweckt = gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar");

        if (istSchonWach || hatAufgeweckt) {
            
            // Wenn er frisch aufgeweckt wurde, schalten wir die Flagge JETZT dauerhaft auf true!
            if (hatAufgeweckt) {
                sessionStorage.setItem("garminAktiviert", "true");
            }

            machPiep(); 
            
            // Das Aktivierungswort wird sauber aus dem Satz herausgeschnitten, falls es mitgesprochen wurde
            const befehlRein = gehoertLower.replace(/okay garmin|ok garmin|okay gar/g, "").trim();
            
            // Feste lokale Befehle prüfen
            if (gehoertLower.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda";
            } else if (gehoertLower.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da";
            } else if (gehoertLower.includes("kilyan")) {
                antwortText = "dummer sack";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("fick deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("video speichern")) {
                antwortText = "sieg heil";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("f*** deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("traubenzucker")) {
                antwortText = "schnupf mehr";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("sieg heil")) {
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd";
            } else if (gehoertLower.includes("schule")) { 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
            } else if (gehoertLower.includes("star wars") || gehoertLower.includes("spiel musik") || gehoertLower.includes("imperium")) { 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1";
                spieleStarWars();
            } else if (gehoertLower.includes("duel of fates") || gehoertLower.includes("schicksal") || gehoertLower.includes("kampf")) { 
                antwortText = "Spiele dein hochgeladenes Duel of the Fates Thema.";
                boxFarbe = "#f8d7da";
                istMusik = true;
                spieleEchtesDuelOfFates(); 
            } else if (gehoertLower.includes("cantina") || gehoertLower.includes("song") || gehoertLower.includes("bar")) { 
                antwortText = "Spiele den Cantina Band Song.";
                boxFarbe = "#fff3cd";
                istMusik = true;
                spieleCantinaSong(); 
            } else if (gehoertLower.includes("hello")) { 
                antwortText = "Spiele Hello Song.";
                boxFarbe = "#fff3cd";
                istMusik = true;
                spieleHello(); 
            } else if (gehoertLower.includes("beenden") || gehoertLower.includes("stopp") || gehoertLower.includes("schlafen")) {
                // EXKLUSIVER GEHEIMBEFEHL: Setzt den Assistenten zurück, sodass er wieder schläft!
                antwortText = "Garmin wird schlafen gelegt. Du musst mich beim nächsten Mal neu aufwecken.";
                boxFarbe = "#d1ecf1";
                sessionStorage.setItem("garminAktiviert", "false"); // Schläft wieder!
                audioPlayer.pause(); 
                rec.stop();
            } else if (befehlRein.length > 0) {
                status.innerText = "🤖 Garmin überlegt...";
                const inputs = window.parent.document.getElementsByTagName('input');
                if (inputs.length > 0) {
                    inputs[0].value = befehlRein;
                    inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                    inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
                    
                    setTimeout(() => {
                        const form = inputs[0].form;
                        if (form) form.requestSubmit();
                    }, 50);
                }
                return;
            }

            if (antwortText) {
                zeigeAntwort(antwortText, boxFarbe, textFarbe);
                if (!istMusik) {
                    setTimeout(() => { sprich(antwortText); }, 250);
                }
            }
        } else {
            status.innerText = "Ignoriert (Du musst Garmin erst einmal mit 'Okay Garmin' aufwecken!): '" + gehoert + "'";
        }
        btn.style.backgroundColor = "#ff4b4b";
    };
    
    rec.onerror = () => { btn.style.backgroundColor = "#ff4b4b"; status.innerText = "Bereit fürs iPad. Klicke zum Sprechen."; };
    rec.onend = () => { btn.style.backgroundColor = "#ff4b4b"; };
}
</script>
"""

# Platzhalter für Musik austauschen
html_bereit = html_reine_web_app.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64)

# Wenn eine KI-Antwort von Python generiert wurde, schleusen wir sie unblockierbar in den Browser ein
if st.session_state.ki_antwort:
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

# Haupt-App rendern
st.components.v1.html(html_bereit, height=270)

